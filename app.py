import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_welcome():
    """Display welcome message"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print("🤖 Interactive AI Chatbot")
    print(f"{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Powered by DeepSeek-V3{Colors.ENDC}")
    print(f"{Colors.WARNING}Type 'exit', 'quit', or 'bye' to end the conversation{Colors.ENDC}")
    print(f"{Colors.WARNING}Type 'clear' to reset conversation history{Colors.ENDC}\n")

def main():
    # Initialize Azure AI client
    endpoint = "https://models.github.ai/inference"
    model = "openai/gpt-5"
    token = os.environ["GITHUB_TOKEN"]
    
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )
    
    # Initialize conversation history
    conversation_history = [
        SystemMessage("You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and engaging responses.")
    ]
    
    print_welcome()
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input(f"{Colors.OKGREEN}{Colors.BOLD}You: {Colors.ENDC}").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print(f"\n{Colors.OKCYAN}👋 Goodbye! Have a great day!{Colors.ENDC}\n")
                break
            
            # Check for clear command
            if user_input.lower() == 'clear':
                conversation_history = [
                    SystemMessage("You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and engaging responses.")
                ]
                print(f"\n{Colors.WARNING}🔄 Conversation history cleared!{Colors.ENDC}\n")
                continue
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Add user message to conversation history
            conversation_history.append(UserMessage(user_input))
            
            # Get AI response
            print(f"{Colors.OKBLUE}{Colors.BOLD}AI: {Colors.ENDC}", end="", flush=True)
            
            response = client.complete(
                messages=conversation_history,
                temperature=1.0,
                top_p=1.0,
                max_tokens=1000,
                model=model
            )
            
            # Extract and display response
            ai_response = response.choices[0].message.content
            print(f"{Colors.OKBLUE}{ai_response}{Colors.ENDC}\n")
            
            # Add assistant response to conversation history
            conversation_history.append(AssistantMessage(ai_response))
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}⚠️  Interrupted by user{Colors.ENDC}")
            print(f"{Colors.OKCYAN}👋 Goodbye! Have a great day!{Colors.ENDC}\n")
            break
        except Exception as e:
            print(f"\n{Colors.FAIL}❌ Error: {str(e)}{Colors.ENDC}\n")
            print(f"{Colors.WARNING}Please try again or type 'exit' to quit.{Colors.ENDC}\n")

if __name__ == "__main__":
    main()

