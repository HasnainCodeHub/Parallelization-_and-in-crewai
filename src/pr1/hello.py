
from crewai.flow.flow import Flow, start, listen, and_
from litellm import completion

class AndAggregationFlow(Flow):
    model = "gemini/gemini-2.0-flash"

    @start()
    def generate_slogan(self):
        # This task generates a creative slogan.
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": "Generate a creative slogan for a futuristic brand."
            }]
        )
        slogan = response["choices"][0]["message"]["content"].strip()
        print("Slogan generated:", slogan)
        return slogan

    @start()
    def generate_tagline(self):
        # This task generates a creative tagline.
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": "Generate a creative tagline for a futuristic brand."
            }]
        )
        tagline = response["choices"][0]["message"]["content"].strip()
        print("Tagline generated:", tagline)
        return tagline




    @listen(and_(generate_slogan, generate_tagline))
    def combine_outputs(self, outputs):
        # Print debug information
        print("Debug - Raw outputs:", outputs)
        
        # Store the results as they're generated
        if not hasattr(self, '_slogan'):
            self._slogan = self.generate_slogan()
        if not hasattr(self, '_tagline'):
            self._tagline = self.generate_tagline()
        
        combined = f"Combined Output: Slogan - '{self._slogan}' | Tagline - '{self._tagline}'"
        print("Aggregated Combined Output:", combined)
        return combined
        
    

    @listen(combine_outputs)
    def save_as_readme(self, outputs):
        with open("README.md", "w") as f:
            f.write(outputs)
            print("README.md file has been created successfully.")
            

def main():
    flow = AndAggregationFlow()
    flow.kickoff()
    print("Final Output of the Flow:")



def plot():
    flow = AndAggregationFlow()
    flow.plot()
    print("Final Output of the Flow:")
