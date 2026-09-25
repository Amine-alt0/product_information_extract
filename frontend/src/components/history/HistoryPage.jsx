import { HistoryIcon } from '../icons/Icons'
import { computeConfidence, parseEquipmentMeta } from '../../utils/formatters'

export default function HistoryPage({ items, onOpen, onNewResearch }) {
  if (!items.length) {
    return (
      <div className="history-page">
        <section className="page-intro">
          <h1>Session history</h1>
          <p>
            Searches from this session appear here. History is cleared when you close or refresh
            the app.
          </p>
        </section>
        <div className="history-empty">
          <HistoryIcon />
          <h2>No research yet</h2>
          <p>Run a search from New Research to build your session history.</p>
          <button type="button" className="btn btn-primary" onClick={onNewResearch}>
            New Research
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="history-page">
      <section className="page-intro">
        <h1>Session history</h1>
        <p>
          {items.length} {items.length === 1 ? 'search' : 'searches'} this session. Select one to
          view results again.
        </p>
      </section>

      <ul className="history-list">
        {items.map((entry) => {
          const meta = parseEquipmentMeta(entry.equipmentName, entry.result)
          const confidence = computeConfidence(entry.result)
          return (
            <li key={entry.id}>
              <button type="button" className="history-item" onClick={() => onOpen(entry)}>
                <div className="history-item-main">
                  <strong>{meta.displayName}</strong>
                  <span>{meta.manufacturer || meta.subcategory || 'Equipment research'}</span>
                </div>
                <div className="history-item-meta">
                  <span className="confidence-badge">{confidence}%</span>
                  <time dateTime={entry.searchedAt}>{formatSessionTime(entry.searchedAt)}</time>
                </div>
              </button>
            </li>
          )
        })}
      </ul>
    </div>
  )
}

function formatSessionTime(iso) {
  try {
    return new Intl.DateTimeFormat(undefined, {
      hour: 'numeric',
      minute: '2-digit',
    }).format(new Date(iso))
  } catch {
    return ''
  }
}
