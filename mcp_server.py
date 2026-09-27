from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

# FastMCP is a high-level library for building MCP servers.
# MCP (Model Context Protocol) is how Claude communicates with external tools and data sources.
mcp = FastMCP("DocumentMCP", log_level="ERROR")


# Simulated document store — in real projects this would be a DB or filesystem.
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# Tools are functions Claude can call during a conversation.
# The @mcp.tool decorator registers this function as an MCP tool.
# `name` and `description` are what Claude sees when deciding whether to use it.

@mcp.tool(
    name="read_doc",
    description="Read the contents of a document and retun it as a string.",
)
def read_docs(
    # Field() lets you attach a description to each parameter — Claude reads these to understand what to pass.
    doc_id: str = Field(..., description="The ID of the document to read.")
):
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]

@mcp.tool(
    name="edit_doc",
    description="Edit the contents byu replacing a string in the douments content with a new string",
)
def edit_doc(
    doc_id: str = Field(..., description="The ID of the document to edit."),
    old_string: str = Field(..., description="The string to be replaced. Must match exactly, including white space"),
    new_string: str = Field(..., description="The string to replace with."),
):
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    docs[doc_id] = docs[doc_id].replace(old_string, new_string)
    return docs[doc_id]

@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def lits_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Rewrites the content of the document in Markdown format.",
)
def format_document(
    doc_id: str=Field(description="The ID of the document to format."),
) -> list[base.Message]:
    prompt = f"""
    Tour goal is to reformat a doument to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in examples, diagrams, and other elements to make the document more engaging and informative. The final output should be a well-structured Markdown document that is easy to read and understand.
    Use the 'edit_document' tool to edit the document. After the documnent has been reformatted, return the final version of the document as a string.
    """
    return [base.UserMessage(prompt)]



# TODO: Write a prompt to summarize a doc


# Start the server using stdio transport — Claude communicates with it via stdin/stdout.
if __name__ == "__main__":
    mcp.run(transport="stdio")
