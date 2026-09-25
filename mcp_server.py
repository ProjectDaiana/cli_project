from pydantic import Field
from mcp.server.fastmcp import FastMCP

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

# TODO: Write a tool to read a doc
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

# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


# Start the server using stdio transport — Claude communicates with it via stdin/stdout.
if __name__ == "__main__":
    mcp.run(transport="stdio")
