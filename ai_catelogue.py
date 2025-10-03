# AI Catalogue for Engine Parts
# By: ChatGPT

class EngineCatalogue:
    def __init__(self):
        # Dictionary to store engine parts
        self.parts = {
            "piston": {
                "category": "Core Component",
                "function": "Converts pressure from combustion into mechanical motion.",
                "material": "Aluminum alloy",
                "price": 120
            },
            "crankshaft": {
                "category": "Core Component",
                "function": "Converts reciprocating motion of pistons into rotational motion.",
                "material": "Forged steel",
                "price": 350
            },
            "spark plug": {
                "category": "Ignition System",
                "function": "Ignites the air-fuel mixture inside the cylinder.",
                "material": "Ceramic & nickel alloy",
                "price": 15
            },
            "valve": {
                "category": "Valve Mechanism",
                "function": "Controls the flow of air/fuel and exhaust gases in cylinders.",
                "material": "Heat-resistant steel",
                "price": 40
            },
            "fuel injector": {
                "category": "Fuel System",
                "function": "Sprays fuel into the combustion chamber in fine mist.",
                "material": "Stainless steel",
                "price": 90
            }
        }

    def search_part(self, query):
        """Search engine part by name"""
        query = query.lower()
        if query in self.parts:
            details = self.parts[query]
            return f"\n🔧 Part: {query.title()}\nCategory: {details['category']}\nFunction: {details['function']}\nMaterial: {details['material']}\nPrice: ${details['price']}\n"
        else:
            return "❌ Part not found in catalogue."

    def search_by_category(self, category):
        """Search engine parts by category"""
        category = category.lower()
        results = [p.title() for p, d in self.parts.items() if d["category"].lower() == category]
        return results if results else ["No parts found in this category."]

    def ai_query(self, question):
        """Simple AI query system"""
        question = question.lower()
        if "price" in question:
            for part in self.parts:
                if part in question:
                    return f"The price of {part.title()} is ${self.parts[part]['price']}."
        elif "function" in question or "do" in question:
            for part in self.parts:
                if part in question:
                    return f"The function of {part.title()} is: {self.parts[part]['function']}"
        elif "category" in question:
            for part in self.parts:
                if part in question:
                    return f"{part.title()} belongs to category: {self.parts[part]['category']}"
        return "I couldn't understand the query. Try asking about price, function, or category."


# Main Program
if __name__ == "__main__":
    catalogue = EngineCatalogue()
    print("🚗 AI Engine Parts Catalogue")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Ask about an engine part (e.g., 'What is the price of piston?'):\n> ")
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break
        elif "category:" in user_input.lower():
            category = user_input.split(":")[-1].strip()
            results = catalogue.search_by_category(category)
            print("🔍 Parts in category:", ", ".join(results))
        elif "search:" in user_input.lower():
            part = user_input.split(":")[-1].strip()
            print(catalogue.search_part(part))
        else:
            print(catalogue.ai_query(user_input))