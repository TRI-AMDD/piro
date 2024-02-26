import withMT from '@material-tailwind/react/utils/withMT';
/** @type {import('tailwindcss').Config} */

module.exports = withMT({
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'dark-black': '#212121', 
        '757575': '#757575'
      },
    },
  },
  variants: {
    extend: {
      select: {
        outlined: {
          label: {
            position: '-top-1.5',
            '&:before': {
              content: '""',
              display: 'block',
              boxSizing: 'border-box',
              width: '2.5px',
              height: '1.5px',
              marginTop: '6.5px',
              marginRight: '0px',
              borderRadius: '4px 0 0 0',
              pointerEvents: 'none',
              transition: 'all',
              borderColor: 'transparent',
            },
            '&:after': {
              content: '""',
              display: 'block',
              flexGrow: '1',
              boxSizing: 'border-box',
              width: '2.5px',
              height: '1.5px',
              marginTop: '6.5px',
              marginLeft: '0px',
              borderRadius: '0 4px 0 0',
              pointerEvents: 'none',
              transition: 'all',
              borderColor: 'transparent',
            },
          },
        },
      },
    },
  },
  plugins: [],
});
