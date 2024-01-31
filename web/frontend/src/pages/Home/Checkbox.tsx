import { FC } from 'react';
import { Checkbox } from '@material-tailwind/react';
import { Control, Controller } from 'react-hook-form';
import { Inputs } from './TypeProps';

export interface CheckBoxProps {
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

const FormCheckbox: FC<CheckBoxProps> = ({ name, control, defaultValue }) => (
  <div>
    <Controller
      name={`${name}`}
      control={control}
      defaultValue={defaultValue}
      render={({ field }) => (
        <Checkbox onBlur={field.onBlur} onChange={field.onChange} checked={field.value} crossOrigin="anonymous" />
      )}
    />
  </div>
);

export default FormCheckbox;
