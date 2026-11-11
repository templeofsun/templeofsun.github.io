/* ============================================================
   TEMPLE OF SUN: shop-postage.js
   Postage prices for the checkout. EDIT THIS FILE BY HAND.

   How to change a price:   change "price" (euro cents: 2200 = €22.00).
   How to move a country:   cut its name from one list, paste it in another.
   How to add a country:    add its name to a list (English name).
   How to add a region:     copy a whole { ... } block and change it.

   A country that is in no list cannot be chosen at checkout; the buyer
   is told to ask Péter instead. Rates researched November 2026, see the
   vault note "Postage from Hungary".
   ============================================================ */
window.TOS_POSTAGE = {
  regions: [
    {
      name: 'Hungary',
      price: 600,
      countries: ['Hungary']
    },
    {
      name: 'Central EU',
      price: 2200,
      countries: [
        'Austria', 'Belgium', 'Croatia', 'Czechia', 'Denmark', 'France',
        'Germany', 'Latvia', 'Lithuania', 'Luxembourg', 'Netherlands',
        'Poland', 'Romania', 'Slovakia', 'Slovenia'
      ]
    },
    {
      name: 'Rest of EU',
      price: 3300,
      countries: [
        'Bulgaria', 'Cyprus', 'Estonia', 'Finland', 'Greece', 'Ireland',
        'Italy', 'Malta', 'Monaco', 'Portugal', 'Spain', 'Sweden'
      ]
    },
    {
      name: 'Europe outside the EU',
      price: 4900,
      note: 'Import tax and customs fees may be charged on delivery.',
      countries: [
        'Albania', 'Andorra', 'Bosnia and Herzegovina', 'Iceland', 'Kosovo',
        'Liechtenstein', 'Moldova', 'Montenegro', 'North Macedonia', 'Norway',
        'San Marino', 'Serbia', 'Switzerland', 'Türkiye', 'Ukraine',
        'United Kingdom', 'Vatican City'
      ]
    }
  ]
};
