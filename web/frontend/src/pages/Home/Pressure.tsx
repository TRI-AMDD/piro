import { useState, useEffect, useMemo, memo } from "react";
import { useForm } from 'react-hook-form';
import { Input } from '@toyota-research-institute/lakefront';
import Select from 'react-select';
import styles from './Home.module.css';

interface Props {
    setPressure(pressure: any): void;
}

const ambientPressure = {
    O2: 0.2095,
    CO2: 0.000394737,
    N2: 0.7809,
    H2: 0.1,
    H2O: 0.1,
    F2: 0.1
}

type PressureInputs = {
    constant: number;
    O2: number;
    CO2: number;
}

const options = [
    { value: 'ambient', label: 'Ambient' },
    { value: 'constant', label: 'Constant' },
    { value: 'custom', label: 'Custom' }
];

export function Pressure(props: Props) {
    const { setPressure } = props;
    const { register, watch } = useForm<PressureInputs>();
    const [option, setOption] = useState<any>(options[0]);
    const watchPressure = watch();

    // compute the pressure based on the option selected
    const pressure = useMemo(() => {
        let pressure: any = ambientPressure;
        if (option?.value === 'constant') {
            pressure = watchPressure.constant ?? 1;
        } else if (option?.value === 'custom') {
            pressure = {
                O2: watchPressure.O2 ?? 0.01,
                CO2: watchPressure.CO2 ?? 0.5
            };
        }
        return pressure;
    }, [watchPressure, option]);

    // trigger a pressure update when pressure has changed
    useEffect(() => { setPressure(pressure); }, [pressure])

    return (
        <div>
            <label>Pressure (atm)</label>
            <Select
                options={options}
                onChange={setOption}
                defaultValue={options[0]}
            />
            <div className={styles.PressureOptions}>
                {option?.value === 'ambient' && (
                    <p>
                        O2: {ambientPressure.O2}<br />
                        CO2: {ambientPressure.CO2}<br />
                        N2: {ambientPressure.N2}<br />
                        H2: {ambientPressure.H2}<br />
                        H2O: {ambientPressure.H2O}<br />
                        F2: {ambientPressure.F2}
                    </p>
                )}

                {option?.value === 'constant' && (
                    <Input
                        type="number"
                        step="any"
                        label="Constant Pressue"
                        defaultValue={1}
                        {...register('constant', { valueAsNumber: true })}
                    />
                )}

                {option?.value === 'custom' && (
                    <>
                        <Input
                            type="number"
                            step="any"
                            label="O2"
                            defaultValue={0.01}
                            {...register('O2', { valueAsNumber: true })}
                        />
                        <Input
                            type="number"
                            step="any"
                            label="CO2"
                            defaultValue={0.5}
                            {...register('CO2', { valueAsNumber: true })}
                        />
                    </>
                )}
            </div>
        </div>
    );
}

const MemoizedPressure = memo(Pressure);
export default MemoizedPressure;
