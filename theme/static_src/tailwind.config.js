/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        income: {
          50:  '#E6F4F0',
          100: '#C0E5DC',
          DEFAULT: '#086B4F',
          600: '#086B4F',
          700: '#065B42',
        },
        expense: {
          50:  '#FCEDEF',
          100: '#F9D0D4',
          DEFAULT: '#E14350',
          600: '#E14350',
          700: '#C83A47',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
