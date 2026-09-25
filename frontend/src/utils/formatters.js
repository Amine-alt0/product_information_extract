export function computeConfidence(result) {
  if (!result) return 0

  let score = 0
  if (result.usage) score += 20
  if (result.caracteristiques_techniques?.length >= 3) score += 30
  else if (result.caracteristiques_techniques?.length > 0) score += 15
  if (result.prix?.valeurs_observees?.length > 0) score += 20
  if (result.sources?.length > 0) score += 20
  if (result.notes && !result.notes.includes('Échec')) score += 10

  return Math.min(score, 99)
}

export function parseEquipmentMeta(equipmentName, result) {
  const name = equipmentName.trim()
  const parts = name.split(/\s+/)
  const manufacturerSource = result?.sources?.find((s) => s.type === 'fabricant')
  const manufacturerFromUrl = manufacturerSource?.url
    ?.replace(/^https?:\/\/(www\.)?/, '')
    .split('/')[0]
    ?.split('.')[0]

  const manufacturer =
    manufacturerFromUrl && manufacturerFromUrl.length > 2
      ? capitalize(manufacturerFromUrl)
      : parts.length > 1
        ? capitalize(parts[0])
        : '—'

  const model = parts.length > 1 ? parts.slice(1).join(' ') : name || '—'

  const category = inferCategory(result)
  const subcategory = inferSubcategory(result, category)

  return {
    displayName: name || 'Unknown equipment',
    manufacturer,
    model,
    category,
    subcategory,
    normalizedName: name || '—',
  }
}

function capitalize(value) {
  if (!value) return '—'
  return value.charAt(0).toUpperCase() + value.slice(1)
}

function inferCategory(result) {
  if (!result?.usage) return 'Industrial equipment'
  const usage = result.usage.toLowerCase()
  if (usage.includes('pompe') || usage.includes('pump')) return 'Pump'
  if (usage.includes('compresseur') || usage.includes('compressor')) return 'Compressor'
  if (usage.includes('ventilateur') || usage.includes('fan')) return 'Fan'
  if (usage.includes('moteur') || usage.includes('motor')) return 'Motor'
  return 'Industrial equipment'
}

function inferSubcategory(result, category) {
  if (!result?.usage) return '—'
  const usage = result.usage.toLowerCase()
  if (category === 'Pump') {
    if (usage.includes('centrifuge')) return 'Centrifugal pump'
    if (usage.includes('vide')) return 'Vacuum pump'
    return 'Pump'
  }
  return category
}

export function formatSourceLabel(source) {
  const labels = {
    fabricant: 'Manufacturer',
    distributeur: 'Distributor',
    document_technique: 'Technical document',
    autre: 'Other',
  }
  return labels[source.type] || 'Source'
}

export function splitNotes(notes) {
  if (!notes?.trim()) return []
  return notes
    .split(/(?<=[.;])\s+/)
    .map((note) => note.trim())
    .filter(Boolean)
}

export function extractApplications(usage) {
  if (!usage) return []
  const segments = usage.split(/[,;]/).map((s) => s.trim()).filter(Boolean)
  if (segments.length <= 1) return []
  return segments.slice(0, 4)
}
