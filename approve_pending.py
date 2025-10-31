import json
import os

APPROVED = "approved.json"
PENDING = "pending.json"

def load_json(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def approve_pending():
    pending = load_json(PENDING)
    approved = load_json(APPROVED)

    if not pending:
        print("No pending ideas to review.")
        return

    print(f"\nReviewing {len(pending)} pending ideas...\n")

    remaining = []
    for idea in pending:
        print(f"Idea ID: {idea['id']}")
        print(f"Idea: {idea['idea']}")
        print(f"Example: {idea['example']}")
        print(f"Author: {idea['author']}")
        choice = input("\nApprove? (y = yes, n = no, s = skip): ").strip().lower()

        if choice == "y":
            approved.append(idea)
            print("Approved!\n")
        elif choice == "n":
            print("Rejected.\n")
        else:
            remaining.append(idea)
            print("⏭ Skipped.\n")

    save_json(APPROVED, approved)
    save_json(PENDING, remaining)
    print("\nDone reviewing!")
    print(f"Approved ideas: {len(approved)} | Remaining pending: {len(remaining)}")

if __name__ == "__main__":
    approve_pending()

