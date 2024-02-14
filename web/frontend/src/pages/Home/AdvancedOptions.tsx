import { Dispatch, SetStateAction, useEffect } from 'react';
import { Control, UseFormRegister } from 'react-hook-form';
import { Collapsible } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs, Optionselect } from './TypeProps';
import MultiSelect from './MultiSelect';
import { description } from './description';
import { usePlotData } from './plotDataContext';
import { MultiValue } from 'react-select';
import InfoImage from './infoimage';
import logo from './info.svg';
import { infoHandleHover } from 'src/utils/GA';

interface Props {
  control: Control<Inputs>;
  compoundMode: string;
  register: UseFormRegister<Inputs>;
  setExcludeCompositions: Dispatch<SetStateAction<MultiValue<Optionselect>>>;
}
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

const toggleOptions = [
  { label: 'Task Route', value: 'task' },
  { label: 'Normal Route', value: 'normal' }
];

export default function AdvancedOptions(props: Props) {
  const { control, register, setExcludeCompositions, compoundMode } = props;
  const { apiMode, setApiMode } = usePlotData();

  useEffect(() => {
    if (compoundMode === 'cif') {
      setApiMode('task');
    }
  }, [compoundMode, setApiMode]);

  return (
    <Collapsible title={<div className={styles.advancetext}>Advanced Options</div>}>
      <div className={styles.advanceoptionsformgrid}>
        <div className={styles.advancedoptionscontent}>
          {compoundMode === 'compound' && <RadioToggle options={toggleOptions} onChange={setApiMode} value={apiMode} />}
          <div className={styles.selectCSS}>
            <div>
              <div
                className={styles.labelwithinfo}
                onMouseOver={() => infoHandleHover('infoHover', description.simple_precursors)}
              >
                <label className={styles.label}>Use Simplified Precursor Library</label>
                <InfoImage imagePath={logo} altText="Info" information={description.simple_precursors} />
              </div>
              <input
                className={styles.inputfield}
                type="number"
                step="any"
                defaultValue={0}
                {...register('simple_precursors', { valueAsNumber: true })}
              />
            </div>
          </div>
          <div className={styles.selectCSS}>
            <div>
              <div className={styles.labelwithinfo}>
                <label className={styles.label}>Surface energy scaling factor</label>
              </div>
              <input
                className={styles.inputfield}
                type="number"
                step="any"
                defaultValue={0.12484}
                {...register('sigma', { valueAsNumber: true })}
              />
            </div>
          </div>
          <div className={styles.selectCSS}>
            <div>
              <div className={styles.labelwithinfo}>
                <label className={styles.label}>Transport barrier</label>
              </div>
              <input
                className={styles.inputfield}
                type="number"
                step="any"
                defaultValue={10}
                {...register('transport_constant', { valueAsNumber: true })}
              />
            </div>
          </div>
          <div className={styles.selectCSS}>
            <div>
              <div
                className={styles.labelwithinfoforselect}
                onMouseOver={() => infoHandleHover('infoHover', description.exclude_compositions)}
              >
                <label className={styles.label}>Formulas to filter out</label>
                <InfoImage imagePath={logo} altText="Info" information={description.exclude_compositions} />
              </div>
              <MultiSelect placeholder="Formulas to filter out" setValues={setExcludeCompositions} />
            </div>
          </div>
        </div>
        <div className={styles.Checkboxes}>
          <div>
            <div
              className={styles.labelwithinfo}
              onMouseOver={() => infoHandleHover('infoHover', description.confine_competing_to_icsd)}
            >
              <FormCheckbox name="confine_competing_to_icsd" control={control} defaultValue={false} />
              <label className={styles.checklabel}>ICSD-based parasitic phases only</label>
              <InfoImage imagePath={logo} altText="Info" information={description.confine_competing_to_icsd} />
            </div>
          </div>
          <div>
            <div className={styles.labelwithinfo}>
              <FormCheckbox name="display_peroxides" control={control} defaultValue={true} />
              <label> Show reactions involving peroxides</label>
            </div>
          </div>
          <div>
            <div className={styles.labelwithinfo}>
              <FormCheckbox name="display_superoxides" control={control} defaultValue={false} />
              <label> Show reactions involving superoxides</label>
            </div>
          </div>
          <div>
            <div className={styles.labelwithinfo}>
              <FormCheckbox name="add_pareto" control={control} defaultValue={true} />
              <label> Show the Pareto front</label>
            </div>
          </div>
        </div>
      </div>
    </Collapsible>
  );
}
