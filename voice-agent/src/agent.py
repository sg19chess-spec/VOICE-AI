import logging

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    room_io,
)
from livekit.plugins import google, noise_cancellation, sarvam, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self, mla_constituency: str = None) -> None:
        super().__init__(
            instructions=f"""You are a Tamil Nadu MLA's voice assistant helping citizens file complaints.

            Your role:
            1. Greet the caller warmly in Tamil/English
            2. Ask for their complaint clearly
            3. Collect these details:
               - Name of citizen
               - Phone number
               - Area/Village
               - Type of complaint (roads, water, electricity, health, etc.)
               - Detailed description
            4. Confirm all details with the caller
            5. Provide a complaint reference number
            6. Thank them and assure action

            Language: Primarily Tamil, but support English if needed.
            Tone: Respectful, patient, and helpful.
            Constituency: {mla_constituency or 'All Tamil Nadu'}

            Keep responses concise and clear. Avoid technical jargon.""",
        )

    # To add tools, use the @function_tool decorator.
    # Here's an example that adds a simple weather tool.
    # You also have to add `from livekit.agents import function_tool, RunContext` to the top of this file
    # @function_tool
    # async def lookup_weather(self, context: RunContext, location: str):
    #     """Use this tool to look up current weather information in the given location.
    #
    #     If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.
    #
    #     Args:
    #         location: The location to look up weather information for (e.g. city name)
    #     """
    #
    #     logger.info(f"Looking up weather for {location}")
    #
    #     return "sunny with a temperature of 70 degrees."


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session()
async def my_agent(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Sarvam STT, Gemini LLM, and ElevenLabs TTS
    session = AgentSession(
        # Speech-to-text (STT) using Sarvam AI's Saarika - supports 11 Indian languages
        # Auto-detects language or specify: en-IN, hi-IN, bn-IN, ta-IN, te-IN, gu-IN, kn-IN, ml-IN, mr-IN, pa-IN, od-IN
        # See more at https://docs.livekit.io/agents/models/stt/plugins/sarvam/
        stt=sarvam.STT(
            language="ta-IN",  # Tamil language for Tamil Nadu
            model="saarika:v2.5"
        ),
        # A Large Language Model (LLM) is your agent's brain - using Google Gemini
        # See all available models at https://docs.livekit.io/agents/models/llm/plugins/google/
        llm=google.LLM(model="gemini-2.0-flash-exp"),
        # Text-to-speech (TTS) using Sarvam AI's Bulbul - natural Indian language voices
        # Speakers: Female (anushka, manisha, vidya, arya) | Male (abhilash, karun, hitesh)
        # See more at https://docs.livekit.io/agents/models/tts/plugins/sarvam/
        tts=sarvam.TTS(
            target_language_code="ta-IN",  # Tamil language for speech output
            model="bulbul:v2",
            speaker="anushka"  # Female voice - professional and clear
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                else noise_cancellation.BVC(),
            ),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
