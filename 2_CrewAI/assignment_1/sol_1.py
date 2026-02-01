from crewai.flow.flow import Flow, start, listen
from crewai import Agent, Task, Crew, Process, LLM
from pydantic import BaseModel
from typing import List

# ---------------- STATE ----------------

class LogisticsState(BaseModel):
    products: List[str] = []
    analysis_report: str = ""
    optimization_plan: str = ""
    completed: bool = False

# ---------------- LLM CONFIGURATION ----------------
llm = LLM(
    model="gemini/gemini-2.5-flash-lite", #"groq/llama-3.1-8b-instant",
    temperature=0.7 
)

# ---------------- AGENTS ----------------

logistics_analyst = Agent(
    role="Logistics Analyst",
    goal="Analyze logistics operations for given products",
    backstory="""
    You are an expert in logistics operations focusing on route efficiency,
    delivery delays, and inventory turnover trends. You identify bottlenecks
    and inefficiencies in supply chains.
    """,
    verbose=True,
    llm=llm
)

optimization_strategist = Agent(
    role="Optimization Strategist",
    goal="Create optimization strategies based on logistics analysis",
    backstory="""
    You specialize in designing actionable optimization strategies using
    route optimization, demand forecasting, and inventory management best practices.
    """,
    verbose=True,
    llm=llm
)


# ---------------- FLOW ----------------

class LogisticsOptimizationFlow(Flow[LogisticsState]):

    @start()
    def initialize(self):
        # Initialize products (can be overridden via kickoff inputs)
        if not self.state.products:
            self.state.products = ["Milk", "Bread", "Frozen Pizza"]
        print("Initialized products:", self.state.products)
        return "initialized"


    @listen(initialize)
    def run_analysis(self, _):

        analysis_task = Task(
            description=f"""
            Analyze current logistics operations for the following products: {self.state.products}.
            Focus on:
            - Route efficiency
            - Delivery delays
            - Inventory turnover trends
            - Key operational bottlenecks
            """,
            expected_output="A structured report summarizing inefficiencies, trends, and key insights.",
            agent=logistics_analyst
        )

        analysis_crew = Crew(
            agents=[logistics_analyst],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )

        result = analysis_crew.kickoff()
        self.state.analysis_report = result.raw
        print("Analysis completed.")
        return "analysis_done"


    @listen(run_analysis)
    def run_optimization(self, _):

        optimization_task = Task(
            description=f"""
            Using the following analysis report:
            {self.state.analysis_report}

            Create an optimization strategy for the products: {self.state.products}.
            Include:
            - Route optimization ideas
            - Inventory management improvements
            - Technology or automation recommendations
            - Expected benefits (cost, time, efficiency)
            """,
            expected_output="A detailed optimization strategy with actionable steps and expected business impact.",
            agent=optimization_strategist
        )

        optimization_crew = Crew(
            agents=[optimization_strategist],
            tasks=[optimization_task],
            process=Process.sequential,
            verbose=True
        )

        result = optimization_crew.kickoff()
        self.state.optimization_plan = result.raw
        self.state.completed = True
        print("Optimization completed.")
        return "optimization_done"


# ---------------- RUN FLOW ----------------

if __name__ == "__main__":
    flow = LogisticsOptimizationFlow()

    flow.kickoff(
        inputs={
            "products": ["Apples", "Bananas", "Ice Cream"]
        }
    )

    print("\nFINAL STATE:")
    print("Analysis Report:\n", flow.state.analysis_report)
    print("\nOptimization Plan:\n", flow.state.optimization_plan)

    with open("./2_CrewAI/assignment_1/report.md", "w") as f:
        f.write("# Logistics Analysis Report\n\n")
        f.write(flow.state.analysis_report)
        f.write("\n\n# Optimization Strategy Plan\n\n")
        f.write(flow.state.optimization_plan)
