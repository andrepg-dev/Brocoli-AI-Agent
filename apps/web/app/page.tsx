'use client'
import { useStream } from '@langchain/langgraph-sdk/react'

export default function WebPage() {
  const stream = useStream({
    apiUrl: 'http://127.0.0.1:2024',
    assistantId: 'agent_graph',
  })

  const handleSubmit = (content: string) => {
    stream.submit(
      { messages: [{ content, type: 'human' }] },
      { streamSubgraphs: true },
    )
  }

  return (
    <div>
      {stream.messages.map((msg) => (
        <pre key={msg.id} className='whitespace-pre font-sans'>
          {JSON.stringify(msg, null, 2)}
        </pre>
      ))}

      <button onClick={() => handleSubmit('Hi, how are you')}>
        Sent question
      </button>
    </div>
  )
}
