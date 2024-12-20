from patterns.singleton.ConfigurationManager import ConfigurationManager
from patterns.command.command_pattern import (
    PreprocessCommand,
    Invoker,
    RunClassifierCommand,
)


# Main function to run the program
def main():
    config_manager = ConfigurationManager()
    # Set up our Command Invoker
    invoker = Invoker()

    while True:
        # Ask the user to choose a model or exit
        print(
            "\nChoose a model to classify your emails or type 'exit' to finish the program.\n"
            "If you haven't already, replace the Email.csv file with your own data.\n"
            "Note: the csv file must be in the same format and renamed to Email.csv."
        )
        print("1. Adaboosting")
        print("2. Voting")
        print("3. SGD")
        print("4. Hist Gradient Boosting")
        print("5. Random Trees Embedding")
        print("Type 'exit' to quit.")

        valid_choices = {"1", "2", "3", "4", "5", "exit"}
        choice = None

        # Handle inputs
        while choice not in valid_choices:
            choice = input("Enter 1, 2, 3, 4, 5, or 'exit': ").strip()
            if choice not in valid_choices:
                print("Invalid input. Please enter a number between 1 and 5, or type 'exit'.")

        # Exits the program
        if choice == "exit":
            print("Exiting the program")
            break
        # Adding preprocessing command to the invoker and executing it
        invoker.add_command(PreprocessCommand())
        invoker.execute_commands()

        # Path to the preprocessed email CSV
        email_csv_path = "data/Emails_preprocessed.csv"

        # Adding run classifier command to the invoker and executing it
        run_classifier_command = RunClassifierCommand(email_csv_path, choice)
        invoker.add_command(run_classifier_command)
        invoker.execute_commands()

        # Output classification results
        predictions = run_classifier_command.get_results()
        print("Classification results:")
        for idx, prediction in enumerate(predictions, start=1):
            print(f"Email {idx}: {prediction}")

        # Finished running all tasks
        print("Finished running all tasks")


if __name__ == "__main__":
    main()
