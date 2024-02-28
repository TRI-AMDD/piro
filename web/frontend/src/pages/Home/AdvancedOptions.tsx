import { Dispatch, SetStateAction } from 'react';
import { Control, UseFormRegister } from 'react-hook-form';
import { useState } from 'react';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs, Optionselect } from './TypeProps';
import MultiSelect from './MultiSelect';
import { description } from './description';
import { MultiValue } from 'react-select';
import InfoImage from './infoimage';
import logo from './info.svg';
import { infoHandleHover } from 'src/utils/GA';
import Collapse from '@mui/material/Collapse';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import IconButton from '@mui/material/IconButton';
import ApiMode from './ApiMode';

interface Props {
  control: Control<Inputs>;
  compoundMode: string;
  register: UseFormRegister<Inputs>;
  setExcludeCompositions: Dispatch<SetStateAction<MultiValue<Optionselect>>>;
}

const AdvancedOptions = (props: Props) => {
  const { control, register, setExcludeCompositions, compoundMode } = props;  
  const collapsibleStyle = { display: 'flex', justifyContent: 'space-between', width: '100%' };
  const iconStyle = { bottom: '5px' };
  const lineStyle = { borderTop: '1px solid #cccccc' };
  const [open, setOpen] = useState<boolean>(false);

  return (
    <div>
      <div className={styles.advancetext} style={collapsibleStyle}>
        Advanced Options
        <IconButton onClick={() => setOpen(!open)} aria-label="expand" size="small" style={iconStyle}>
          {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
        </IconButton>
      </div>
      <div style={lineStyle}></div>
      <div className={styles.advanceoptionsformgrid}>
        <Collapse in={open} timeout="auto" unmountOnExit>
          <div className={styles.advanceoptionsformgrid}>
            <div className={styles.advancedoptionscontent}>
              <ApiMode compoundMode={compoundMode} />
              <div className={styles.selectCSS}>
                <div>
                  <div
                    className={styles.labelwithinfo}
                    onMouseOver={() => infoHandleHover('infoHover', description.simple_precursors)}
                  >
                    <label className={styles.label}>Use Simplified Precursor Library</label>
                    <InfoImage imagePath={logo} altText="Info" information={description.simple_precursors} />
                  </div>
                  <input
                    className={styles.inputfield}
                    type="number"
                    step="any"
                    defaultValue={0}
                    {...register('simple_precursors', { valueAsNumber: true })}
                  />
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinfo}>
                    <label className={styles.label}>Surface energy scaling factor</label>
                  </div>
                  <input
                    className={styles.inputfield}
                    type="number"
                    step="any"
                    defaultValue={0.12484}
                    {...register('sigma', { valueAsNumber: true })}
                  />
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinfo}>
                    <label className={styles.label}>Transport barrier</label>
                  </div>
                  <input
                    className={styles.inputfield}
                    type="number"
                    step="any"
                    defaultValue={10}
                    {...register('transport_constant', { valueAsNumber: true })}
                  />
                </div>
              </div>
              <div className={styles.selectCSS}>
                <div>
                  <div
                    className={styles.labelwithinfoforselect}
                    onMouseOver={() => infoHandleHover('infoHover', description.exclude_compositions)}
                  >
                    <label className={styles.label}>Formulas to filter out</label>
                    <InfoImage imagePath={logo} altText="Info" information={description.exclude_compositions} />
                  </div>
                  <MultiSelect placeholder="Formulas to filter out" setValues={setExcludeCompositions} />
                </div>
              </div>
            </div>
            <div className={styles.Checkboxes}>
              <div>
                <div
                  className={styles.labelwithinfo}
                  onMouseOver={() => infoHandleHover('infoHover', description.confine_competing_to_icsd)}
                >
                  <FormCheckbox name="confine_competing_to_icsd" control={control} defaultValue={false} />
                  <label className={styles.checklabel}>ICSD-based parasitic phases only</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.confine_competing_to_icsd} />
                </div>
              </div>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="display_peroxides" control={control} defaultValue={true} />
                  <label> Show reactions involving peroxides</label>
                </div>
              </div>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="display_superoxides" control={control} defaultValue={false} />
                  <label> Show reactions involving superoxides</label>
                </div>
              </div>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="add_pareto" control={control} defaultValue={true} />
                  <label> Show the Pareto front</label>
                </div>
              </div>
            </div>
          </div>
        </Collapse>
      </div>
    </div>
  );
};

export default AdvancedOptions;
