import { FC } from 'react';
import { Checkbox } from '@toyota-research-institute/lakefront';
import { Control, Controller } from 'react-hook-form';
import { Inputs } from './TypeProps';

export interface CheckboxProps {
    label: string;
    name:
        | 'allowGasRelease'
        | 'showFractionKnownPrecursors'
        | 'showKnownPrecursorsOnly'
        | 'confineCompetingToIcsd'
        | 'displayPeroxides'
        | 'addPareto';
    control: Control<Inputs>;
}

const FormCheckbox: FC<CheckboxProps> = ({ name, control, label }) => (
    <div>
        <Controller
            name={name}
            control={control}
            defaultValue={false}
            render={({ field }) => (
                <Checkbox onBlur={field.onBlur} onChange={field.onChange} checked={field.value} label={label} />
            )}
        />
    </div>
);

export default FormCheckbox;
