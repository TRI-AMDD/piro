import { useState, useEffect, useMemo, memo } from 'react';
import { useForm } from 'react-hook-form';
import { description } from './description';
import styles from './Home.module.css';
import { PressureType } from './TypeProps';
import { Select, Option } from '@material-tailwind/react';
import InfoImage from './infoimage';
import logo from './info.svg';
import { infoHandleHover } from 'src/utils/GA';

interface Props {
  setPressure(pressure: PressureType | number): void;
}

const ambientPressure = {
  O2: 0.2095,
  CO2: 0.000394737,
  N2: 0.7809,
  H2: 0.1,
  H2O: 0.1,
  F2: 0.1
};

type PressureInputs = {
  constant: number;
  O2: number;
  CO2: number;
  N2: number;
  H2: number;
  H2O: number;
  F2: number;
};
interface Option {
  label: string;
  value: string;
}
const options = [
  { value: 'ambient', label: 'Ambient' },
  { value: 'constant', label: 'Constant' },
  { value: 'custom', label: 'Custom' }
];

export function Pressure(props: Props) {
  const { setPressure } = props;
  const { register, watch } = useForm<PressureInputs>();
  const [option, setOption] = useState<Option | undefined>(() => options[0]);
  const watchPressure = watch();

  // compute the pressure based on the option selected
  const pressure = useMemo(() => {
    let pressure: PressureType | number = ambientPressure;
    if (option?.value === 'constant') {
      pressure = watchPressure.constant ?? 1;
    } else if (option?.value === 'custom') {
      pressure = {
        O2: watchPressure.O2 ?? 0.01,
        CO2: watchPressure.CO2 ?? 0.5,
        N2: watchPressure.N2 ?? 1,
        H2: watchPressure.H2 ?? 1,
        H20: watchPressure.H2O ?? 1,
        F2: watchPressure.F2 ?? 1
      };
    }
    return pressure;
  }, [watchPressure, option]);

  // trigger a pressure update when pressure has changed
  useEffect(() => {
    setPressure(pressure);
  }, [pressure, setPressure]);

  return (
    <div>
      <div className={styles.selectCSS}>
        <div>
          <div
            className={styles.labelwithinfoforselect}
            onMouseOver={() => infoHandleHover('infoHover', description.pressure)}
          >
            <label className={styles.label}>Pressure (atm)</label>
            <InfoImage imagePath={logo} altText="Info" information={description.pressure} />
          </div>
          <Select
            className={styles.singleselect}
            placeholder="Additional element"
            value={option?.value || ''}
            onChange={(value) => setOption(options.find((option) => option.value === value))}
          >
            {options.map((option) => (
              <Option key={option.value} value={option.value}>
                {option.label}
              </Option>
            ))}
          </Select>
        </div>
      </div>
      <div className={styles.PressureOptions}>
        {option?.value === 'ambient' && (
          <p>
            O2: {ambientPressure.O2}
            <br />
            CO2: {ambientPressure.CO2}
            <br />
            N2: {ambientPressure.N2}
            <br />
            H2: {ambientPressure.H2}
            <br />
            H2O: {ambientPressure.H2O}
            <br />
            F2: {ambientPressure.F2}
          </p>
        )}

        {option?.value === 'constant' && (
          <div className={styles.selectCSS}>
            <div>
              <div className={styles.labelwithinfoforselect}>
                <label className={styles.labelpressure}>Constant Pressure</label>
              </div>
              <input
                type="number"
                step="any"
                className={styles.inputfieldpressure}
                defaultValue={1}
                {...register('constant', { valueAsNumber: true })}
              />
            </div>
          </div>
        )}

        {option?.value === 'custom' && (
          <>
            <div className={styles.custumgap}>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinputTWO}>
                    <label className={styles.labelpressure}>O2</label>

                    <input
                      type="number"
                      step="any"
                      className={styles.inputfieldpressure}
                      defaultValue={0.01}
                      {...register('O2', { valueAsNumber: true })}
                    />
                  </div>
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinputTHREE}>
                    <label className={styles.labelpressure}>CO2</label>

                    <input
                      type="number"
                      step="any"
                      className={styles.inputfieldpressure}
                      defaultValue={0.5}
                      {...register('CO2', { valueAsNumber: true })}
                    />
                  </div>
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinputTWO}>
                    <label className={styles.labelpressure}>N2</label>
                    <input
                      type="number"
                      step="any"
                      className={styles.inputfieldpressure}
                      defaultValue={1}
                      {...register('N2', { valueAsNumber: true })}
                    />
                  </div>
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinputTWO}>
                    <label className={styles.labelpressure}>H2</label>
                    <input
                      type="number"
                      step="any"
                      className={styles.inputfieldpressure}
                      defaultValue={1}
                      {...register('H2', { valueAsNumber: true })}
                    />
                  </div>
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinputTHREE}>
                    <label className={styles.labelpressure}>H2O</label>
                    <input
                      type="number"
                      step="any"
                      className={styles.inputfieldpressure}
                      defaultValue={1}
                      {...register('H2O', { valueAsNumber: true })}
                    />
                  </div>
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinputTWO}>
                    <label className={styles.labelpressure}>F2</label>
                    <input
                      type="number"
                      step="any"
                      className={styles.inputfieldpressure}
                      defaultValue={1}
                      {...register('F2', { valueAsNumber: true })}
                    />
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

const MemoizedPressure = memo(Pressure);
export default MemoizedPressure;
