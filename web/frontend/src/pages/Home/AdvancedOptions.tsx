import { Control, UseFormRegister } from 'react-hook-form';
import { Collapsible, Input } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs } from './TypeProps';
import MultiSelect from './MultiSelect';
import MoreInfo from './MoreInfo';
import { description } from './description';

interface Props {
    control: Control<Inputs>;
    register: UseFormRegister<Inputs>;
    setExcludeCompositions(input: { label: string; value: string; }[]): void;
}

export default function AdvancedOptions(props: Props) {
    const { control, register, setExcludeCompositions } = props;

    return (
        <Collapsible
            title="Advanced Options"
        >
            <div className={styles.FormGrid}>
                <div>
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
                        <MultiSelect
                            label="Formulas to filter out"
                            setValues={setExcludeCompositions}
                        />
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
                    <FormCheckbox
                        name="add_pareto"
                        control={control}
                        label="Show the Pareto front"
                        defaultValue={true}
                    />
                </div>
            </div>
        </Collapsible>
    );
}
