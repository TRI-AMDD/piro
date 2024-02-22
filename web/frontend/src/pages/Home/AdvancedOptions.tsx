import { Dispatch, SetStateAction, useEffect } from 'react';
import { Control, UseFormRegister } from 'react-hook-form';
import { Collapsible } from '@toyota-research-institute/lakefront';
import { Button } from '@material-tailwind/react';
import KeyboardArrowDownOutlinedIcon from '@mui/icons-material/KeyboardArrowDownOutlined';
import { useState } from 'react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Link, Typography } from '@mui/material';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs, Optionselect } from './TypeProps';
import MultiSelect from './MultiSelect';
import { description } from './description';
import { usePlotData } from './plotDataContext';
import { MultiValue } from 'react-select';
import InfoImage from './infoimage';
import logo from './info.svg';
import { infoHandleHover } from 'src/utils/GA';
import Card from "@mui/material/Card";
import Collapse from "@mui/material/Collapse";
import CardHeader from "@mui/material/CardHeader";
import Container from "@mui/material/Container";
import CardContent from "@mui/material/CardContent";
import KeyboardArrowDownIcon from
    "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowUpIcon from
    "@mui/icons-material/KeyboardArrowUp";
import IconButton from "@mui/material/IconButton";

interface Props {
  control: Control<Inputs>;
  compoundMode: string;
  register: UseFormRegister<Inputs>;
  setExcludeCompositions: Dispatch<SetStateAction<MultiValue<Optionselect>>>;
}
interface Option {
  label: string;
  value: string;
}

interface RadioToggleProps {
  options: Option[];
  onChange: (value: string) => void;
  value: string;
}

const RadioToggle: React.FC<RadioToggleProps> = ({ options, onChange, value }) => {
  return (
    <div className={styles.radiobuttons}>
      {options.map((option) => (
        <div key={option.value} className="mb-2 flex items-center">
          <input
            type="radio"
            id={option.value}
            value={option.value}
            checked={value === option.value}
            onChange={() => onChange(option.value)}
            className={styles.custumradio}
          />
          <label htmlFor={option.value} className="ml-2">
            {option.label}
          </label>
        </div>
      ))}
    </div>
  );
};

const isProd = import.meta.env.MODE === 'production';

const toggleOptions = [
  { label: 'Task Route', value: 'task' },
  { label: 'Normal Route', value: 'normal' }
];

const AdvancedOptions = (props) => {
  const { control, register, setExcludeCompositions, compoundMode } = props;
  const { apiMode, setApiMode } = usePlotData();
  const collapsibleStyle = { display: "flex", justifyContent: "space-between", width:"100%"};
  const iconStyle = { bottom : "5px"};
  const lineStyle = { borderTop: "1px solid #cccccc"};
  const [open, setOpen] = useState<boolean>(false);
  useEffect(() => {
    if (compoundMode === 'cif') {
      setApiMode('task');
    }
  }, [compoundMode, setApiMode]);






 return (
<div>
 <div className={styles.advancetext} style = {collapsibleStyle}>Advanced Options
  <IconButton onClick={() => setOpen(!open)}  aria-label="expand" size="small" style = {iconStyle}>
  {open ? <KeyboardArrowUpIcon />: <KeyboardArrowDownIcon />}</IconButton></div>
  <div style={lineStyle}></div>
                 <div className={styles.advanceoptionsformgrid}>
                     <Collapse in={open} timeout="auto"
                         unmountOnExit>
                             <div className={styles.advanceoptionsformgrid}>
                             <div className={styles.advancedoptionscontent}>
                                   {compoundMode === 'compound' && (
                                       <RadioToggle
                                          options={isProd ? toggleOptions.filter((itr) => itr.value != 'task') : toggleOptions}
                                          onChange={setApiMode}
                                          value={isProd ? 'normal' : apiMode}
                                        />
                                               )}
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
}

export default AdvancedOptions;
