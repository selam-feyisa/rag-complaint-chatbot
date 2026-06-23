import gradio as gr
from src.rag_pipeline import retrieve_and_answer

# Chat with memory
def chat_with_memory(message, history):
    if not message or message.strip() == "":
        return history + [("Please ask a question.", "")]
    
    answer, sources, _ = retrieve_and_answer(message)
    sources_text = "\n".join(sources)
    
    response = f"""
**🤖 AI Analysis**

{answer}

---

**📚 Sources Used:**
{sources_text}
"""
    history.append((message, response))
    return history

# Modern ChatGPT-style UI
with gr.Blocks(
    title="CrediTrust AI",
    theme=gr.themes.Soft(primary_hue="emerald", secondary_hue="violet")
) as demo:
    
    gr.HTML("""
    <div style="text-align: center; padding: 30px 20px 20px;">
        <h1 style="color: #34d399; margin: 0;">🏦 CrediTrust</h1>
        <h2 style="color: white; margin: 10px 0 5px;">Intelligent Complaint Analyzer</h2>
        <p style="color: #94a3b8; font-size: 17px;">Real customer insights at your fingertips</p>
    </div>
    """)
    
    chatbot = gr.Chatbot(
        height=650,
        label="💬 Conversation",
        avatar_images=["🧑‍💼", "🤖"]
    )
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your question here... (e.g. Why are there so many complaints about Credit Cards?)",
            label="Your Message",
            lines=2,
            scale=8
        )
        submit = gr.Button("🚀 Send", variant="primary", scale=1)
    
    with gr.Row():
        clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
    
    # Examples
    gr.Examples(
        examples=[
            ["Why are people complaining about Credit Cards?"],
            ["What are the top issues with Personal Loans?"],
            ["How are customers feeling about Money Transfers?"],
            ["Summarize complaints about Savings Accounts"],
        ],
        inputs=msg,
        label="💡 Suggested Questions"
    )
    
    # Interactions
    submit.click(
        chat_with_memory,
        inputs=[msg, chatbot],
        outputs=chatbot
    ).then(lambda: "", None, msg)  # Clear input after send
    
    msg.submit(
        chat_with_memory,
        inputs=[msg, chatbot],
        outputs=chatbot
    ).then(lambda: "", None, msg)
    
    clear_btn.click(lambda: [], None, chatbot)
    
    gr.Markdown("**Built for CrediTrust Financial • 10 Academy Week 7**")

if __name__ == "__main__":
    demo.launch(share=False)