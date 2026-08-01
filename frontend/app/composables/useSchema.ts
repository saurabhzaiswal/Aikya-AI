export function useSchema(schema: Record<string, unknown> | Array<Record<string, unknown>>): void {
  const schemas = Array.isArray(schema) ? schema : [schema]
  useHead({
    script: schemas.map(item => ({
      type: 'application/ld+json',
      // Escaping '<' prevents static JSON-LD from being interpreted as an HTML closing tag.
      innerHTML: JSON.stringify(item).replace(/</g, '\\u003c'),
    })),
  })
}
