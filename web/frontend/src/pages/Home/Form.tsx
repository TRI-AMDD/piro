import { Dispatch } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Button, Input } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs } from './TypeProps';

interface Props {
    setRequest: Dispatch<any>;
}

export default function Form(props: Props) {
    const { setRequest } = props;
    const {
        control,
        register,
        handleSubmit,
        formState: { errors }
    } = useForm<Inputs>();

    const onSubmit: SubmitHandler<Inputs> = (data) => {
        // set the form request to trigger an api call
        setRequest(data);
    };

    return (
        /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
        <form onSubmit={handleSubmit(onSubmit)} className={styles.Form}>
            <Input
                label="Formula"
                {...register('formula', { required: true })}
                error={errors.formula ? 'Formula field is required' : ''}
            />
            <h3>Advanced Options</h3>
            <div className={styles.FormGrid}>
                <div>
                    <Input type="number" label="Temperature (K)" {...register('temperature')} placeholder="1600" />
                    <Input type="number" label="Pressure (atm)" {...register('pressure')} placeholder="0.001" />
                    <Input label="Add element" {...register('add_elements')} placeholder="None" />
                    <Input label="Max precursors" {...register('max_component_precursors')} placeholder="2" />
                </div>
                <div className={styles.Checkboxes}>
                    <FormCheckbox
                        name="allowGasRelease"
                        control={control}
                        label="Allow for gaseous reaction products, e.g. O2, CO2"
                    />
                    <FormCheckbox
                        name="showFractionKnownPrecursors"
                        control={control}
                        label="Show the fraction of known synthetic reagents in reaction"
                    />
                    <FormCheckbox
                        name="showKnownPrecursorsOnly"
                        control={control}
                        label="Show only reactions with known precursors"
                    />
                    <FormCheckbox
                        name="confineCompetingToIcsd"
                        control={control}
                        label="Confine competing reactions to those containing ICSD materials"
                    />
                    <FormCheckbox
                        name="displayPeroxides"
                        control={control}
                        label="Show reactions involving peroxide compounds"
                    />
                    <FormCheckbox
                        name="addPareto"
                        control={control}
                        label="Show the Pareto front on the reaction analysis diagram"
                    />
                </div>
            </div>

            <Button type="submit">Run</Button>
        </form>
    );
}
