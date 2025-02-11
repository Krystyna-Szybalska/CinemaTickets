/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#000',
        },
      },
    }
  },
  defaults: {
    VBtn: {
      rounded: 'xl',
      variant: 'flat',
      color: '#000',
      height: 44,
    },
    VTextField: {
      rounded: 4,
      hideDetails: true,
      density: 'compact',
      variant: 'outlined',
      validateOn: 'blur',
    },
    VSelect: {
      rounded: 4,
      hideDetails: true,
      density: 'compact',
      variant: 'outlined',
      validateOn: 'blur',
      itemColor: 'primary',
      menuProps: {
        maxHeight: 300,
      },
    },
  },
})
