module.exports = {
  content: [
    './templates/**/*.html',  // para que o Tailwind escaneie seus templates HTML
    './static/**/*.js'        // caso tenha scripts JS que usem classes do Tailwind
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

