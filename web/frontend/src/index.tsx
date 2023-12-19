import { createRoot } from 'react-dom/client';
import 'tailwindcss/tailwind.css';
import App from './app';
import { ThemeProvider } from '@material-tailwind/react';


const container = document.getElementById('root') as HTMLDivElement;
const root = createRoot(container);

root.render(
    <ThemeProvider>
      <App />
    </ThemeProvider>
);
