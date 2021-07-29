import { useForm, SubmitHandler } from 'react-hook-form';
import { UseMutationResult } from "react-query";
import { Button, Input } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs } from './TypeProps';
import { useState } from "react";
import MultiSelect from "./MultiSelect";
import AdvancedOptions from "./AdvancedOptions";
import Pressure from "./Pressure";

interface Props {
    mutation: UseMutationResult<any, unknown, void, unknown>;
}

export default function Form(props: Props) {
    const { mutation } = props;
    const [pressure, setPressure] = useState<any>(null);
    const [addElements, setAddElements] = useState<{ label: string; value: string; }[]>([]);
    const [explicitIncludes, setExplicitIncludes] = useState<{ label: string; value: string; }[]>([]);
    const [excludeCompositions, setExcludeCompositions] = useState<{ label: string; value: string; }[]>([]);

    const {
        control,
        register,
        handleSubmit,
        formState: { errors },
        watch
    } = useForm<Inputs>();

    // watch to disable hull_distance
    const watchConfineToStables = watch('confine_to_stables', true);

    const onSubmit: SubmitHandler<Inputs> = (data) => {
        // set values from multi-select values
        data.add_elements = addElements.map(e => e.value);
        data.explicit_includes = explicitIncludes.map(e => e.value);
        data.exclude_compositions = excludeCompositions.map(e => e.value);
        // get value from pressure
        data.pressure = pressure;

        // @ts-ignore
        // set the form request to trigger an api call
        mutation.mutate(data);
    };

    return (
        /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
        <form onSubmit={handleSubmit(onSubmit)} className={styles.Form}>
            <div className={styles.FormGrid}>
                <div>
                    <Input
                        label="Target Compound (mp-id)"
                        placeholder="mp-9029"
                        {...register('target_entry_id', { required: true })}
                        error={errors.target_entry_id ? 'Formula field is required' : ''}
                    />
                    <Input
                        type="number"
                        step="any"
                        label="Temperature (K)"
                        placeholder="1000"
                        {...register('temperature', { valueAsNumber: true })}
                    />
                    <Input
                        label="Maximum number of components in precursors"
                        {...register('max_component_precursors', { valueAsNumber: true })}
                        defaultValue={0}
                    />
                    <Input
                        label="Depth of parasitic reaction search"
                        {...register('flexible_competition', { valueAsNumber: true })}
                        defaultValue={0}
                    />
                    <Input
                        label="Distance to Hull (eV/atom)"
                        {...register('hull_distance', { valueAsNumber: true })}
                        disabled={watchConfineToStables}
                        placeholder="0.01"
                    />
                    <MultiSelect
                        label="Additional element to consider"
                        placeholder="Type element and press enter e.g. (C, H)"
                        setValues={setAddElements}
                    />
                    <MultiSelect
                        label="Explicitly include as precursor"
                        setValues={setExplicitIncludes}
                    />
                </div>
                <div className={styles.Checkboxes}>
                    <FormCheckbox
                        name="allow_gas_release"
                        control={control}
                        label="Allow for gaseous reaction products"
                        defaultValue={false}
                    />
                    <FormCheckbox
                        name="show_fraction_known_precursors"
                        control={control}
                        label="Show the fraction of known precursors in reaction"
                        defaultValue={false}
                    />
                    <FormCheckbox
                        name="show_known_precursors_only"
                        control={control}
                        label="Show only reactions with known precursors"
                        defaultValue={false}
                    />
                    <FormCheckbox
                        name="confine_to_stables"
                        control={control}
                        label="Stable Precursors Only"
                        defaultValue={true}
                    />
                    <FormCheckbox
                        name="confine_to_icsd"
                        control={control}
                        label="ICSD-based Precursors Only"
                        defaultValue={true}
                    />
                </div>
                <Pressure setPressure={setPressure} />
            </div>
            <AdvancedOptions control={control} register={register} setExcludeCompositions={setExcludeCompositions} />

            <Button type="submit">Run</Button>
        </form>
    );
}
