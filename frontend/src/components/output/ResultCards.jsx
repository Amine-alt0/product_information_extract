import { ExternalLinkIcon, InfoIcon, LinkIcon, NoteIcon, TagIcon, WrenchIcon } from '../icons/Icons'
import { extractApplications, formatSourceLabel, splitNotes } from '../../utils/formatters'

function CardShell({ icon: Icon, title, children, className = '' }) {
  return (
    <article className={`result-card ${className}`}>
      <header className="result-card-header">
        <Icon />
        <h3>{title}</h3>
      </header>
      {children}
    </article>
  )
}

function DataRow({ label, value }) {
  return (
    <div className="data-row">
      <span>{label}</span>
      <strong>{value || '—'}</strong>
    </div>
  )
}

export function IdentificationCard({ meta, confidence }) {
  return (
    <CardShell icon={InfoIcon} title="Identification">
      <div className="card-body">
        <DataRow label="Manufacturer" value={meta.manufacturer} />
        <DataRow label="Model" value={meta.model} />
        <DataRow label="Category" value={meta.category} />
        <DataRow label="Subcategory" value={meta.subcategory} />
        <DataRow label="Normalized name" value={meta.normalizedName} />
        <div className="confidence-block">
          <div className="confidence-label">
            <span>Confidence score</span>
            <strong>{confidence}%</strong>
          </div>
          <div className="confidence-bar">
            <span style={{ width: `${confidence}%` }} />
          </div>
        </div>
      </div>
    </CardShell>
  )
}

export function TechnicalInfoCard({ specs = [] }) {
  return (
    <CardShell icon={WrenchIcon} title="Technical Information">
      <div className="card-body spec-grid">
        {specs.length === 0 ? (
          <p className="empty-state">No technical specifications found.</p>
        ) : (
          specs.map((spec) => (
            <div key={`${spec.nom}-${spec.valeur}`} className="spec-item">
              <span>{spec.nom}</span>
              <strong>{spec.valeur}</strong>
              {spec.source && <em>{spec.source}</em>}
            </div>
          ))
        )}
      </div>
    </CardShell>
  )
}

export function PurposeCard({ usage }) {
  const applications = extractApplications(usage)

  return (
    <CardShell icon={TagIcon} title="Purpose & Applications">
      <div className="card-body">
        <p className="usage-text">{usage || 'No usage information available.'}</p>
        {applications.length > 0 && (
          <>
            <h4>Typical applications</h4>
            <ul className="bullet-list">
              {applications.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </>
        )}
      </div>
    </CardShell>
  )
}

export function MarketInfoCard({ prix }) {
  const prices = prix?.valeurs_observees ?? []
  const sources = prix?.sources ?? []

  return (
    <CardShell icon={TagIcon} title="Market Information">
      <div className="card-body">
        <DataRow
          label="Estimated price range"
          value={prices.length ? prices.join(' · ') : '—'}
        />
        <DataRow
          label="Price source"
          value={sources.length ? sources.join(', ') : '—'}
        />
        <DataRow label="Currency" value={detectCurrency(prices)} />
        <DataRow label="Date" value={new Date().toLocaleDateString('en-GB')} />
        {prix?.note && <p className="muted-note">{prix.note}</p>}
      </div>
    </CardShell>
  )
}

export function SourcesCard({ sources = [] }) {
  return (
    <CardShell icon={LinkIcon} title="Sources">
      <div className="card-body">
        {sources.length === 0 ? (
          <p className="empty-state">No sources cited.</p>
        ) : (
          <ul className="source-list">
            {sources.map((source) => (
              <li key={source.url}>
                <a href={source.url} target="_blank" rel="noreferrer">
                  <span>{formatSourceLabel(source)} — {getDomain(source.url)}</span>
                  <ExternalLinkIcon />
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </CardShell>
  )
}

export function NotesCard({ notes }) {
  const items = splitNotes(notes)

  return (
    <CardShell icon={NoteIcon} title="Notes">
      <div className="card-body">
        {items.length === 0 ? (
          <p className="empty-state">No additional notes.</p>
        ) : (
          <ul className="bullet-list">
            {items.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        )}
      </div>
    </CardShell>
  )
}

function getDomain(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, '')
  } catch {
    return url
  }
}

function detectCurrency(prices) {
  const joined = prices.join(' ')
  if (joined.includes('€') || joined.toUpperCase().includes('EUR')) return 'EUR'
  if (joined.includes('$') || joined.toUpperCase().includes('USD')) return 'USD'
  if (joined.toUpperCase().includes('GBP') || joined.includes('£')) return 'GBP'
  return '—'
}

export const RESULT_SECTIONS = [
  { id: 'identification', label: 'Identification', component: 'identification' },
  { id: 'technical', label: 'Technical Information', component: 'technical' },
  { id: 'usage', label: 'Usage & Applications', component: 'usage' },
  { id: 'market', label: 'Market Information', component: 'market' },
  { id: 'sources', label: 'Sources', component: 'sources' },
  { id: 'notes', label: 'Notes', component: 'notes' },
]

export function renderResultSection(sectionId, props) {
  switch (sectionId) {
    case 'identification':
      return <IdentificationCard meta={props.meta} confidence={props.confidence} />
    case 'technical':
      return <TechnicalInfoCard specs={props.result.caracteristiques_techniques} />
    case 'usage':
      return <PurposeCard usage={props.result.usage} />
    case 'market':
      return <MarketInfoCard prix={props.result.prix} />
    case 'sources':
      return <SourcesCard sources={props.result.sources} />
    case 'notes':
      return <NotesCard notes={props.result.notes} />
    default:
      return null
  }
}
