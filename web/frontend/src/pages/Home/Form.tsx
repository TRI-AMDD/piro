import { useForm, SubmitHandler } from 'react-hook-form';
import { UseMutationResult } from "react-query";
import { Button, Input } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs } from './TypeProps';
import { useState } from "react";
import MultiSelect from "./MultiSelect";

interface Props {
    mutation: UseMutationResult<any, unknown, void, unknown>;
}

export default function Form(props: Props) {
    const { mutation } = props;
    const [elements, setElements] = useState<{ label: string; value: string; }[]>([]);

    const {
        control,
        register,
        handleSubmit,
        formState: { errors }
    } = useForm<Inputs>();

    const onSubmit: SubmitHandler<Inputs> = (data) => {
        // set add_elements values
        data.add_elements = elements.map(e => e.value);

        // add various inputs

        // @ts-ignore
        // set the form request to trigger an api call
        mutation.mutate(data);
    };

    return (
        /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
        <form onSubmit={handleSubmit(onSubmit)} className={styles.Form}>
            <Input
                label="Target Compound (mp-id)"
                placeholder="mp-9029"
                {...register('target_entry_id', { required: true })}
                error={errors.target_entry_id ? 'Formula field is required' : ''}
            />
            <h3>Advanced Options</h3>
            <div className={styles.FormGrid}>
                <div>
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
                    <MultiSelect
                        label="Additional element to consider"
                        placeholder="Type element and press enter e.g. (C, H)"
                        setValues={setElements}
                    />
                    <Input
                        type="number"
                        step="any"
                        label="Pressure (atm)"
                        {...register('pressure', { valueAsNumber: true })}
                        defaultValue={0.001}
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
                    <FormCheckbox
                        name="confine_competing_to_icsd"
                        control={control}
                        label="ICSD-based Parasitic Phases Only"
                        defaultValue={false}
                    />
                    <FormCheckbox
                        name="display_peroxides"
                        control={control}
                        label="Show reactions involving peroxides"
                        defaultValue={true}
                    />
                    <FormCheckbox
                        name="add_pareto"
                        control={control}
                        label="Show the Pareto front"
                        defaultValue={true}
                    />
                </div>
            </div>

            <Button type="submit">Run</Button>
        </form>
    );
}
