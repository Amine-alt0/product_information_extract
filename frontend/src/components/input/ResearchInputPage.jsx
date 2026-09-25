import { useState } from 'react'
import { DocumentIcon, GridIcon, SearchIcon, SparkIcon, IllustrationIcon } from '../icons/Icons'

const FEATURES = [
  {
    icon: SparkIcon,
    title: 'AI-Powered Research',
    description: 'Automatically search and extract equipment information',
  },
  {
    icon: GridIcon,
    title: 'Structured Results',
    description: 'Get organized technical specs, pricing, and sources',
  },
  {
    icon: DocumentIcon,
    title: 'Professional Reports',
    description: 'Generate inspection-ready documentation',
  },
]

const MAX_HINT_LENGTH = 500

export default function ResearchInputPage({ onSubmit,oncancel, isLoading, error }) {
  const [equipmentName, setEquipmentName] = useState('')
  const [hint, setHint] = useState('')

  function handleSubmit(event) {
    event.preventDefault()
    if (!equipmentName.trim() || isLoading) return
    onSubmit(equipmentName, hint)
  }

  return (
    <div className="input-page">
      <section className="page-intro">
        <h1>Research Equipment</h1>
        <p>
          Enter an equipment name or model to automatically search and extract technical
          information, pricing, and documentation.
        </p>
      </section>

      <section className="feature-bar">
        {FEATURES.map(({ icon: Icon, title, description }) => (
          <article key={title} className="feature-card">
            <div className="feature-icon">
              <Icon />
            </div>
            <div>
              <h3>{title}</h3>
              <p>{description}</p>
            </div>
          </article>
        ))}
      </section>

      <section className="search-panel">
        <form className="search-form-card" onSubmit={handleSubmit}>
          <h2>What are you researching?</h2>

          <label className="field">
            <span>Equipment, product or model name *</span>
            <input
              type="text"
              value={equipmentName}
              onChange={(event) => setEquipmentName(event.target.value)}
              placeholder="e.g. Grundfos CR 15-4"
              required
              disabled={isLoading}
            />
          </label>

          <label className="field">
            <span>Additional information (optional)</span>
            <textarea
              value={hint}
              onChange={(event) => setHint(event.target.value.slice(0, MAX_HINT_LENGTH))}
              placeholder="Add context such as manufacturer, application, or location to improve results..."
              rows={4}
              disabled={isLoading}
            />
            <span className="char-count">
              {hint.length}/{MAX_HINT_LENGTH}
            </span>
          </label>

          {error && (
            <div className="form-error-box" role="alert">
              <strong>Research failed</strong>
              <p>{error}</p>
            </div>
          )}

          {isLoading && (
            <p className="loading-note">
              Running the equipment pipeline — this can take a minute depending on search and AI calls.
            </p>
          )}

          <button type="submit" className="btn btn-primary btn-block" disabled={isLoading || !equipmentName.trim()}>
            <SearchIcon />
            {isLoading ? 'Researching…' : 'Start Research'}
          </button>
          <button type="button" className="btn  btn-block btn-cancel" disabled={!isLoading} onClick={oncancel}>
            
            {isLoading ? 'Cancel' : 'Cancel'}
          </button>
        </form>

        <aside className="search-illustration-card">
          <IllustrationIcon />
          <h3>Find the information you need</h3>
          <p>
            Our AI searches manufacturer websites, technical documentation, and market data to
            provide comprehensive equipment intelligence.
          </p>
        </aside>
      </section>
    </div>
  )
}
