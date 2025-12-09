from typing import List, Dict
import re


def parse_vtt_file(content: str) -> tuple[str, List[dict]]:
    """Parse VTT file and extract transcript with speakers"""
    lines = content.split('\n')
    transcript_parts = []
    participants = {}

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip WEBVTT header and empty lines
        if line.startswith('WEBVTT') or line == '' or '-->' in line:
            i += 1
            continue

        # Check if line contains speaker info (e.g., "<v John>")
        speaker_match = re.match(r'<v\s+([^>]+)>', line)
        if speaker_match:
            speaker = speaker_match.group(1).strip()
            text = re.sub(r'<v\s+[^>]+>', '', line).strip()

            # Add to participants
            if speaker not in participants:
                participants[speaker] = {"name": speaker, "email": None}

            transcript_parts.append(f"{speaker}: {text}")
        elif line and not line.isdigit():
            transcript_parts.append(line)

        i += 1

    full_transcript = '\n'.join(transcript_parts)
    participant_list = list(participants.values())

    return full_transcript, participant_list
