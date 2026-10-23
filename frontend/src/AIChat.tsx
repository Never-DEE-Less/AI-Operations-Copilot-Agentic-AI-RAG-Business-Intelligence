
import { useState, type FormEvent } from 'react'
import './AIChat.css'


const API_URL = 'http://127.0.0.1:8000'

type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}

const suggestions = [
  'Which category generated the most revenue?',
  'Show me the monthly revenue trend.',
  'Who are our top five customers by revenue?',
]

export default function AIChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function sendQuestion(
    event?: FormEvent<HTMLFormElement>,
    suggestedQuestion?: string,
  ) {
    event?.preventDefault()

    const text = (suggestedQuestion ?? question).trim()
    if (!text || loading) return

    setMessages((previous) => [
      ...previous,
      { role: 'user', content: text },
    ])
    setQuestion('')
    setError('')
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/ai/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text }),
      })

      if (!response.ok) {
        throw new Error(`Request failed (${response.status}).`)
      }

      const data: { answer: string } = await response.json()

      setMessages((previous) => [
        ...previous,
        { role: 'assistant', content: data.answer },
      ])
    } catch {
      setError(
        'Could not reach the AI assistant. Check that FastAPI and Ollama are running.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="ai-chat panel" id="ai-assistant">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">ASK YOUR BUSINESS DATA</p>
          <h2>AI Operations Assistant</h2>
        </div>
        <span className="ai-badge">Local LLM</span>
      </div>

      <p className="ai-description">
        Ask a business question in plain English. Answers are generated using
        your approved analytics tools.
      </p>

      {messages.length === 0 && (
        <div className="suggestion-list">
          <p>Try asking</p>
          {suggestions.map((suggestion) => (
            <button
              className="suggestion"
              key={suggestion}
              type="button"
              disabled={loading}
              onClick={() => void sendQuestion(undefined, suggestion)}
            >
              <span>{suggestion}</span>
              <span aria-hidden="true">↗</span>
            </button>
          ))}
        </div>
      )}

      <div className="chat-messages" aria-live="polite">
        {messages.map((message, index) => (
          <article
            className={`chat-message ${message.role}`}
            key={`${index}-${message.role}`}
          >
            <span className="message-role">
              {message.role === 'user' ? 'YOU' : 'AI ASSISTANT'}
            </span>
            <p>{message.content}</p>
          </article>
        ))}

        {loading && (
          <div className="chat-loading" role="status">
            Qwen is analysing your question…
          </div>
        )}
      </div>

      {error && <p className="chat-error" role="alert">{error}</p>}

      <form className="chat-form" onSubmit={(event) => void sendQuestion(event)}>
        <input
          aria-label="Ask a business question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask about revenue, categories, or customers…"
          maxLength={1000}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? 'Thinking…' : 'Ask AI ↗'}
        </button>
      </form>

      <p className="chat-disclaimer">
        The assistant can make mistakes. Verify important figures against the
        analytics dashboard.
      </p>
    </section>
  )
}
