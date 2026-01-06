#!/usr/bin/env python3
"""
Persona Tuner - CLI for quick persona adjustments
Usage: python persona_tuner.py <persona_id> <attribute> <value>
Example: python persona_tuner.py phil_dandy base_pitch 0.98
"""
import json
import sys
from pathlib import Path

def tune_persona(persona_id: str, attribute: str, value: float):
    """Quick and dirty persona tuning without web UI"""

    skg_path = Path(__file__).parent / "skg" / "skg_core.json"

    if not skg_path.exists():
        print(f"❌ SKG file not found: {skg_path}")
        return

    with open(skg_path, 'r') as f:
        skg = json.load(f)

    persona = None
    persona_type = None

    if persona_id in skg["personas"]:
        persona = skg["personas"][persona_id]
        persona_type = "primary"
    elif persona_id in skg["standby_personas"]:
        persona = skg["standby_personas"][persona_id]
        persona_type = "standby"
    else:
        print(f"❌ Persona {persona_id} not found")
        print(f"Available personas: {list(skg['personas'].keys()) + list(skg['standby_personas'].keys())}")
        return

    # Update voice profile
    updated = False
    if attribute in ["base_pitch", "speaking_rate"]:
        persona["voice_profile"][attribute] = value
        updated = True
    elif attribute.startswith("formant_"):
        formant = attribute.split("_")[1]
        if "formant_shifts" not in persona["voice_profile"]:
            persona["voice_profile"]["formant_shifts"] = {}
        persona["voice_profile"]["formant_shifts"][formant] = value
        updated = True
    elif attribute == "interruptibility":
        persona["persona_traits"][attribute] = value
        updated = True

    if not updated:
        print(f"❌ Unknown attribute: {attribute}")
        print("Available attributes: base_pitch, speaking_rate, formant_f1, formant_f2, formant_f3, interruptibility")
        return

    # Save changes
    with open(skg_path, 'w') as f:
        json.dump(skg, f, indent=2)

    print(f"✅ Updated {persona_type} persona {persona_id}: {attribute} = {value}")

def list_personas():
    """List all available personas"""
    skg_path = Path(__file__).parent / "skg" / "skg_core.json"

    if not skg_path.exists():
        print(f"❌ SKG file not found: {skg_path}")
        return

    with open(skg_path, 'r') as f:
        skg = json.load(f)

    print("🎭 Primary Personas:")
    for pid, persona in skg["personas"].items():
        print(f"  {pid}: {persona['name']} ({persona['role']})")

    print("\n🎭 Standby Personas:")
    for pid, persona in skg["standby_personas"].items():
        print(f"  {pid}: {persona['name']} ({persona['role']})")

def show_persona_details(persona_id: str):
    """Show detailed information about a persona"""
    skg_path = Path(__file__).parent / "skg" / "skg_core.json"

    if not skg_path.exists():
        print(f"❌ SKG file not found: {skg_path}")
        return

    with open(skg_path, 'r') as f:
        skg = json.load(f)

    persona = None
    if persona_id in skg["personas"]:
        persona = skg["personas"][persona_id]
    elif persona_id in skg["standby_personas"]:
        persona = skg["standby_personas"][persona_id]

    if not persona:
        print(f"❌ Persona {persona_id} not found")
        return

    print(f"🎭 Persona: {persona['name']} ({persona_id})")
    print(f"Role: {persona['role']}")
    print("\nVoice Profile:")
    for key, value in persona["voice_profile"].items():
        print(f"  {key}: {value}")
    print("\nPersona Traits:")
    for key, value in persona["persona_traits"].items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Persona Tuner - CLI for quick persona adjustments")
        print("\nCommands:")
        print("  python persona_tuner.py list                          # List all personas")
        print("  python persona_tuner.py show <persona_id>             # Show persona details")
        print("  python persona_tuner.py <persona_id> <attribute> <value>  # Update persona")
        print("\nExamples:")
        print("  python persona_tuner.py phil_dandy base_pitch 0.98")
        print("  python persona_tuner.py jim_dandy speaking_rate 1.05")
        print("  python persona_tuner.py tech_expert formant_f1 1.1")
        print("\nAvailable attributes:")
        print("  base_pitch, speaking_rate, formant_f1, formant_f2, formant_f3, interruptibility")
        sys.exit(0)

    if sys.argv[1] == "list":
        list_personas()
    elif sys.argv[1] == "show" and len(sys.argv) == 3:
        show_persona_details(sys.argv[2])
    elif len(sys.argv) == 4:
        try:
            value = float(sys.argv[3])
            tune_persona(sys.argv[1], sys.argv[2], value)
        except ValueError:
            print(f"❌ Invalid value: {sys.argv[3]} (must be a number)")
            sys.exit(1)
    else:
        print("❌ Invalid command format")
        print("Use 'python persona_tuner.py' for help")
        sys.exit(1)