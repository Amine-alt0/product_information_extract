import { ArrowLeftIcon } from '../icons/Icons'

import { RESULT_SECTIONS, renderResultSection } from './ResultCards'



export default function ResultsPage({ result, meta, confidence, onBack }) {

  const cardProps = { result, meta, confidence }



  return (

    <div className="results-page">

      <button type="button" className="back-link" onClick={onBack}>

        <ArrowLeftIcon />

        Back to search

      </button>



      <section className="product-header-card">

        <div className="product-visual">

          <div className="product-image-placeholder" aria-hidden="true">

            <svg viewBox="0 0 120 160" fill="none">

              <rect x="42" y="20" width="36" height="120" rx="8" fill="#E2E8F0" />

              <rect x="34" y="12" width="52" height="18" rx="6" fill="#CBD5E1" />

              <rect x="48" y="140" width="24" height="10" rx="4" fill="#94A3B8" />

              <circle cx="60" cy="70" r="14" fill="#F8FAFC" stroke="#94A3B8" strokeWidth="2" />

            </svg>

          </div>

        </div>



        <div className="product-summary">

          <div className="product-title-row">

            <div>

              <div className="title-with-badge">

                <h1>{meta.displayName}</h1>

                <span className="confidence-badge">Confidence: {confidence}%</span>

              </div>

              <p className="product-subtitle">{meta.subcategory}</p>

            </div>

          </div>



          <div className="product-meta-row">

            <MetaItem label="Manufacturer" value={meta.manufacturer} />

            <MetaItem label="Category" value={meta.category} />

            <MetaItem label="Subcategory" value={meta.subcategory} />

            <MetaItem label="Normalized name" value={meta.normalizedName} />

          </div>

        </div>

      </section>



      <div className="results-grid">

        {RESULT_SECTIONS.map((section) => (

          <div key={section.id}>{renderResultSection(section.id, cardProps)}</div>

        ))}

      </div>

    </div>

  )

}



function MetaItem({ label, value }) {

  return (

    <div className="meta-item">

      <span>{label}</span>

      <strong>{value}</strong>

    </div>

  )

}

