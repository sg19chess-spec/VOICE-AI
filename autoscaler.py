#!/usr/bin/env python3
"""
RunPod Auto-Scaler for Tamil Nadu MLA Voice Agent
Automatically scales RunPod instances based on load
"""

import os
import time
import requests
import logging
from typing import Dict, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RunPodAutoScaler:
    """Manages RunPod instance scaling based on agent load"""

    # Scaling thresholds
    SCALING_RULES = {
        'small': {
            'gpu': 'RTX 3070',
            'max_concurrent': 30,
            'cost_per_hour': 0.30,
            'template_id': 'runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04'
        },
        'medium': {
            'gpu': 'RTX 4070',
            'max_concurrent': 80,
            'cost_per_hour': 0.45,
            'template_id': 'runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04'
        },
        'large': {
            'gpu': 'RTX 4080',
            'max_concurrent': 150,
            'cost_per_hour': 0.60,
            'template_id': 'runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04'
        },
        'xlarge': {
            'gpu': 'RTX 4090',
            'max_concurrent': 240,
            'cost_per_hour': 0.69,
            'template_id': 'runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04'
        }
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.runpod.io/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.current_pod_id: Optional[str] = None
        self.current_size: str = 'small'
        self.idle_start_time: Optional[float] = None
        self.IDLE_TIMEOUT = 1800  # 30 minutes

    def get_livekit_metrics(self) -> Dict:
        """Get current metrics from LiveKit server"""
        try:
            # Query LiveKit server for current sessions
            livekit_url = os.getenv('LIVEKIT_URL', 'http://localhost:7880')
            response = requests.get(f"{livekit_url}/stats")

            if response.status_code == 200:
                data = response.json()
                return {
                    'active_sessions': data.get('num_rooms', 0),
                    'total_participants': data.get('num_participants', 0),
                }
            return {'active_sessions': 0, 'total_participants': 0}
        except Exception as e:
            logger.error(f"Failed to get LiveKit metrics: {e}")
            return {'active_sessions': 0, 'total_participants': 0}

    def determine_required_size(self, active_sessions: int) -> str:
        """Determine what instance size is needed"""
        if active_sessions == 0:
            return 'none'  # Can shut down
        elif active_sessions <= 30:
            return 'small'
        elif active_sessions <= 80:
            return 'medium'
        elif active_sessions <= 150:
            return 'large'
        else:
            return 'xlarge'

    def create_pod(self, size: str) -> Optional[str]:
        """Create a new RunPod instance"""
        config = self.SCALING_RULES[size]

        query = """
        mutation {
          podFindAndDeployOnDemand(
            input: {
              cloudType: SECURE
              gpuTypeId: "%s"
              name: "tn-mla-voice-%s"
              dockerArgs: ""
              ports: "7880/http,7881/http,443/http,3478/udp,50000:60000/udp"
              volumeInGb: 50
              containerDiskInGb: 50
              env: [
                {key: "LIVEKIT_API_KEY", value: "%s"},
                {key: "LIVEKIT_API_SECRET", value: "%s"},
                {key: "SARVAM_API_KEY", value: "%s"},
                {key: "GOOGLE_API_KEY", value: "%s"}
              ]
            }
          ) {
            id
            machineId
            machine {
              gpuDisplayName
            }
          }
        }
        """ % (
            config['gpu'],
            size,
            os.getenv('LIVEKIT_API_KEY'),
            os.getenv('LIVEKIT_API_SECRET'),
            os.getenv('SARVAM_API_KEY'),
            os.getenv('GOOGLE_API_KEY')
        )

        try:
            response = requests.post(
                self.base_url,
                json={'query': query},
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                pod_id = data['data']['podFindAndDeployOnDemand']['id']
                logger.info(f"✅ Created {size} pod: {pod_id}")
                return pod_id
            else:
                logger.error(f"Failed to create pod: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error creating pod: {e}")
            return None

    def stop_pod(self, pod_id: str):
        """Stop a RunPod instance"""
        query = f"""
        mutation {{
          podStop(input: {{podId: "{pod_id}"}}) {{
            id
          }}
        }}
        """

        try:
            response = requests.post(
                self.base_url,
                json={'query': query},
                headers=self.headers
            )

            if response.status_code == 200:
                logger.info(f"⏸️  Stopped pod: {pod_id}")
                return True
            else:
                logger.error(f"Failed to stop pod: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error stopping pod: {e}")
            return False

    def scale(self):
        """Main scaling logic"""
        metrics = self.get_livekit_metrics()
        active_sessions = metrics['active_sessions']
        required_size = self.determine_required_size(active_sessions)

        logger.info(f"📊 Active sessions: {active_sessions}, Current: {self.current_size}, Required: {required_size}")

        # Handle idle timeout
        if active_sessions == 0:
            if self.idle_start_time is None:
                self.idle_start_time = time.time()
                logger.info(f"⏰ Idle timer started")
            elif time.time() - self.idle_start_time > self.IDLE_TIMEOUT:
                if self.current_pod_id:
                    logger.info(f"💤 Idle timeout reached, stopping pod")
                    self.stop_pod(self.current_pod_id)
                    self.current_pod_id = None
                    self.current_size = 'none'
                self.idle_start_time = None
        else:
            self.idle_start_time = None

        # Scale up if needed
        if required_size != 'none' and required_size != self.current_size:
            logger.info(f"📈 Scaling from {self.current_size} to {required_size}")

            # Stop current pod if exists
            if self.current_pod_id:
                self.stop_pod(self.current_pod_id)

            # Create new pod
            new_pod_id = self.create_pod(required_size)
            if new_pod_id:
                self.current_pod_id = new_pod_id
                self.current_size = required_size

                # Estimate cost
                config = self.SCALING_RULES[required_size]
                monthly_cost = config['cost_per_hour'] * 720  # 24/7
                business_days_cost = config['cost_per_hour'] * 264  # Business days

                logger.info(f"💰 Estimated cost: ${monthly_cost:.2f}/month (24/7) or ${business_days_cost:.2f}/month (business days)")

    def run(self, interval: int = 300):
        """Run auto-scaler continuously"""
        logger.info(f"🚀 Starting RunPod Auto-Scaler")
        logger.info(f"📊 Checking every {interval} seconds")

        while True:
            try:
                self.scale()
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("👋 Shutting down auto-scaler")
                break
            except Exception as e:
                logger.error(f"Error in scaling loop: {e}")
                time.sleep(60)  # Wait a bit before retrying


if __name__ == "__main__":
    # Get RunPod API key from environment
    api_key = os.getenv('RUNPOD_API_KEY')

    if not api_key:
        logger.error("❌ RUNPOD_API_KEY environment variable not set")
        exit(1)

    # Verify other required env vars
    required_vars = ['LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET', 'SARVAM_API_KEY', 'GOOGLE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        exit(1)

    # Create and run auto-scaler
    scaler = RunPodAutoScaler(api_key)
    scaler.run(interval=300)  # Check every 5 minutes
