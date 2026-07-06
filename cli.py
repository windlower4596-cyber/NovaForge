import sys
import os
import argparse
from backend.app.security import validate_user_idea
from backend.app.agents.inventor import InventorAgent
from backend.app.agents.engineer import EngineerAgent
from backend.app.agents.economist import EconomistAgent
from backend.app.agents.critic import CriticAgent
from backend.app.agents.pitch_gen import PitchGeneratorAgent

# ANSI Colors for terminal output
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_banner():
    print(BOLD + BLUE + """
======================================================
  _   _                 ______                     
 | \ | |               |  ____|                    
 |  \| | _____   ____ _| |__ ___  _ __ __ _  ___   
 | . ` |/ _ \ \ / / _` |  __/ _ \| '__/ _` |/ _ \  
 | |\  | (_) \ V / (_| | | | (_) | | | (_| |  __/  
 |_| \_|\___/ \_/ \__,_|_|  \___/|_|  \__, |\___|  
                                       __/ |       
    NOVAFORGE AI - AGENT CLI INTERFACE|___/        
======================================================
""" + RESET)

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="NovaForge AI Multi-Agent Offline CLI Generator")
    parser.add_argument(
        "--idea", "-i",
        type=str,
        required=True,
        help="The innovation idea to transform into a proposal."
    )
    parser.add_argument(
        "--out", "-o",
        type=str,
        default="proposal_output.md",
        help="Output filepath for the compiled markdown proposal."
    )
    args = parser.parse_args()

    print(f"{BOLD}[System]{RESET} Validating input idea...")
    
    # 1. Input Validation & Sanitization (Security Features)
    try:
        validated_idea = validate_user_idea(args.idea)
        print(f"{GREEN}[OK]{RESET} Input validated successfully.")
    except Exception as e:
        print(f"{RED}[ERR] Security Validation Error:{RESET} {str(e)}")
        sys.exit(1)

    # 2. Initialize Agents
    print(f"\n{BOLD}[System]{RESET} Initializing Google ADK Agent team...")
    inventor = InventorAgent()
    engineer = EngineerAgent()
    economist = EconomistAgent()
    critic = CriticAgent()
    pitch_gen = PitchGeneratorAgent()

    context = {}
    agent_sequence = [inventor, engineer, economist, critic, pitch_gen]

    # 3. Coordinate pipeline execution
    print(f"{BOLD}[System]{RESET} Starting sequential execution pipeline...\n")
    
    for agent in agent_sequence:
        print(f"{BOLD}{BLUE}>>> Agent Active: {agent.name}{RESET}")
        print(f"{YELLOW}Persona Details: {agent.description}{RESET}")
        print(f"{BOLD}Reasoning Logs:{RESET}")
        
        try:
            # Run the agent
            result = agent.run(validated_idea, context)
            
            # Print intermediate logs
            for line in result.get("logs", "").split("\n"):
                print(f"  {line}")
            print(f"{GREEN}Completed {agent.name}{RESET}\n")
            
            context[agent.name] = result
        except Exception as e:
            print(f"{RED}[ERR] Error running agent {agent.name}: {str(e)}{RESET}")
            sys.exit(1)

    # 4. Save compilation
    final_output = context.get("Pitch Generator Agent", {}).get("output", "")
    if final_output:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(final_output)
            print(f"{BOLD}{GREEN}[OK] Multi-agent execution finished successfully!{RESET}")
            print(f"Final proposal written to: {BOLD}{os.path.abspath(args.out)}{RESET}")
        except Exception as e:
            print(f"{RED}[ERR] Failed to write output file: {str(e)}{RESET}")
            sys.exit(1)
    else:
        print(f"{RED}[ERR] Pipeline finished but no output was compiled.{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
