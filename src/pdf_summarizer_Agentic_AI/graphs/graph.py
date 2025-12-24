from langgraph.graph import StateGraph, START, END
from src.pdf_summarizer_Agentic_AI.states.state import AgentState
from src.pdf_summarizer_Agentic_AI.nodes.node import AgentNodes

class GraphBuilder:
    def __init__(self, model):
        """Init with the specific LLM model instance."""
        self.llm = model
        self.nodes = AgentNodes()
        self.graph_builder = StateGraph(AgentState)

    def build_summarization_workflow(self):
        """Defines the nodes and edges for the graph."""
        self.graph_builder.add_node("loader", self.nodes.data_loader_node)
        self.graph_builder.add_node("summarizer", self.nodes.summarizer_node)

        self.graph_builder.add_edge(START, "loader")
        self.graph_builder.add_edge("loader", "summarizer")
        self.graph_builder.add_edge("summarizer", END)

    def setup_graph(self):
        """Compiles the graph."""
        self.build_summarization_workflow()
        return self.graph_builder.compile()