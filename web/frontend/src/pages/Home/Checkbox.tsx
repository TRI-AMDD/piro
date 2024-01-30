import { FC } from 'react';
import { Checkbox } from '@toyota-research-institute/lakefront';
import { Control, Controller } from 'react-hook-form';
import { Inputs } from './TypeProps';

export interface CheckboxProps {
  name:
    | 'confine_to_icsd'
    | 'confine_to_stables'
    | 'allow_gas_release'
    | 'show_fraction_known_precursors'
    | 'show_known_precursors_only'
    | 'confine_competing_to_icsd'
    | 'display_peroxides'
    | 'display_superoxides'
    | 'add_pareto';
  control: Control<Inputs>;
  defaultValue: boolean;
}

const FormCheckbox: FC<CheckboxProps> = ({ name, control, defaultValue }) => (
  <div>
    <Controller
      name={`${name}`}
      control={control}
      defaultValue={defaultValue}
      render={({ field }) => <Checkbox onBlur={field.onBlur} onChange={field.onChange} checked={field.value} />}
    />
  </div>
);

export default FormCheckbox;
