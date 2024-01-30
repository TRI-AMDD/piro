import React from 'react';

interface Option {
  label: string;
  value: string;
}

interface RadioToggleProps {
  options: Option[];
  onChange: (value: string) => void;
  value: string;
}

export const RadioToggle: React.FC<RadioToggleProps> = ({ options, onChange, value }) => {
  return (
    <div>
      {options.map((option) => (
        <div key={option.value} className="mb-2 flex items-center">
          <input
            type="radio"
            id={option.value}
            value={option.value}
            checked={value === option.value}
            onChange={() => onChange(option.value)}
            className="form-radio h-5 w-5 text-blue-500"
          />
          <label htmlFor={option.value} className="ml-2">
            {option.label}
          </label>
        </div>
      ))}
    </div>
  );
};

