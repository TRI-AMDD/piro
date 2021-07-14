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
        console.log(data);
        // make api call here
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
            <Input type="number" label="Temperature" {...register('temperature')} placeholder="1600 K" />
            <Input type="number" label="Pressure" {...register('pressure')} placeholder="0.001 atm" />
            <Input label="Add element" {...register('addElement')} placeholder="None" />
            <Input label="Max precursors" {...register('precursors')} placeholder="2" />

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

            <Button type="submit">Run</Button>
        </form>
    );
}
