import { Dispatch, SetStateAction, useEffect } from 'react';
import { Control, UseFormRegister } from 'react-hook-form';
import { Collapsible, Input, Toggle } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs, Option } from './TypeProps';
import MultiSelect from './MultiSelect';
import MoreInfo from './MoreInfo';
import { description } from './description';
import { usePlotData } from './plotDataContext';
import { MultiValue } from 'react-select';

interface Props {
  control: Control<Inputs>;
  compoundMode: string;
  register: UseFormRegister<Inputs>;
  setExcludeCompositions: Dispatch<SetStateAction<MultiValue<Option>>>;
}

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
    <Collapsible title="Advanced Options">
      <div className={styles.advanceoptionsformgrid}>
        <div>
          {compoundMode === 'compound' && <Toggle options={toggleOptions} onChange={setApiMode} value={apiMode} />}
          <MoreInfo info={description.simple_precursors}>
            <Input
              type="number"
              step="any"
              label="Use Simplified Precursor Library"
              defaultValue={0}
              {...register('simple_precursors', { valueAsNumber: true })}
            />
          </MoreInfo>
          <Input
            type="number"
            step="any"
            label="Surface energy scaling factor"
            defaultValue={0.12484}
            {...register('sigma', { valueAsNumber: true })}
          />
          <Input
            type="number"
            step="any"
            label="Transport barrier"
            defaultValue={10}
            {...register('transport_constant', { valueAsNumber: true })}
          />
          <MoreInfo info={description.exclude_compositions}>
            <MultiSelect label="Formulas to filter out" setValues={setExcludeCompositions} />
          </MoreInfo>
        </div>
        <div className={styles.Checkboxes}>
          <MoreInfo info={description.confine_competing_to_icsd} isCheckbox>
            <FormCheckbox
              name="confine_competing_to_icsd"
              control={control}
              label="ICSD-based Parasitic Phases Only"
              defaultValue={false}
            />
          </MoreInfo>
          <FormCheckbox
            name="display_peroxides"
            control={control}
            label="Show reactions involving peroxides"
            defaultValue={true}
          />
          <FormCheckbox
            name="display_superoxides"
            control={control}
            label="Show reactions involving superoxides"
            defaultValue={false}
          />
          <FormCheckbox name="add_pareto" control={control} label="Show the Pareto front" defaultValue={true} />
        </div>
      </div>
    </Collapsible>
  );
}
