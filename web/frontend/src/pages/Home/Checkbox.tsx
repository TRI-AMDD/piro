import { FC } from 'react';
import { Checkbox } from '@toyota-research-institute/lakefront';
import { Control, Controller } from 'react-hook-form';
import { Inputs } from './TypeProps';

export interface CheckboxProps {
    label: string;
    name:
        | 'allow_gas_release'
        | 'show_fraction_known_precursors'
        | 'show_known_precursors_only'
        | 'confine_competing_to_icsd'
        | 'display_peroxides'
        | 'add_pareto';
    control: Control<Inputs>;
    defaultValue: boolean;
}

const FormCheckbox: FC<CheckboxProps> = ({ name, control, label , defaultValue}) => (
    <div>
        <Controller
            name={`synthesis_bool_options.${name}`}
            control={control}
            defaultValue={defaultValue}
            render={({ field }) => (
                <Checkbox onBlur={field.onBlur} onChange={field.onChange} checked={field.value} label={label} />
            )}
        />
    </div>
);

export default FormCheckbox;
