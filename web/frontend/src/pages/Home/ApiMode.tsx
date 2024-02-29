import { useEffect } from 'react';
import styles from './Home.module.css';
import { usePlotData } from './plotDataContext';

interface Option {
  label: string;
  value: string;
}

interface RadioToggleProps {
  options: Option[];
  onChange: (value: string) => void;
  value: string;
}

const RadioToggle: React.FC<RadioToggleProps> = ({ options, onChange, value }) => {
  return (
    <div className={styles.radiobuttons}>
      {options.map((option) => (
        <div key={option.value} className="mb-2 flex items-center">
          <input
            type="radio"
            id={option.value}
            value={option.value}
            checked={value === option.value}
            onChange={() => onChange(option.value)}
            className={styles.custumradio}
          />
          <label htmlFor={option.value} className="ml-2">
            {option.label}
          </label>
        </div>
      ))}
    </div>
  );
};

const isProd = import.meta.env.MODE === 'production';

const toggleOptions = [
  { label: 'Task Route', value: 'task' },
  { label: 'Normal Route', value: 'normal' }
];

interface Props {
  compoundMode: string;
}

const ApiMode = (props: Props) => {
  const { compoundMode } = props;
  const { apiMode, setApiMode } = usePlotData();

  useEffect(() => {
    if (compoundMode === 'cif') {
      setApiMode('task');
    }
  }, [compoundMode, setApiMode]);

  if (compoundMode !== 'compound') {
    return null;
  }

  if (isProd) {
    return null;
  }

  return <RadioToggle options={toggleOptions} onChange={setApiMode} value={isProd ? 'normal' : apiMode} />;
};

export default ApiMode;
