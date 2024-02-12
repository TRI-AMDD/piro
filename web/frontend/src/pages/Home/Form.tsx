import { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Button } from '@material-tailwind/react';
import { Toggle } from '@toyota-research-institute/lakefront';
import { Option } from '@material-tailwind/react';
import { Tooltip } from 'react-tooltip';
import logo from './info.svg';
import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs, PressureType, Optionselect } from './TypeProps';
import InfoImage from './infoimage';
import MultiSelect from './MultiSelect';
import AdvancedOptions from './AdvancedOptions';
import Pressure from './Pressure';
import { description } from './description';
import { usePlotData } from './plotDataContext';
import { MultiValue } from 'react-select';
import React, { useRef } from 'react';
import SingleSelect from './SingleSelect';

const addElementOptions = [
  { value: '', label: 'None' },
  { value: 'C', label: 'C' },
  { value: 'O', label: 'O' }
];

const toggleOptions = [
  { label: 'Upload Target Compound (.cif)', value: 'compound' },
  { label: 'Upload Target Compound (.cif)', value: 'cif' }
];
interface Option {
  label: string;
  value: string;
}
export default function Form() {
  const { mutation } = usePlotData();
  const [pressure, setPressure] = useState<PressureType | null | number>(null);
  const [addElements, setAddElements] = useState<Option>(addElementOptions[0]);
  const [explicitIncludes, setExplicitIncludes] = useState<MultiValue<Optionselect>>([]);
  const [excludeCompositions, setExcludeCompositions] = useState<MultiValue<Optionselect>>([]);
  const [compoundMode, setCompoundMode] = useState('compound');
  const [cifString, setCifString] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

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
    data.add_elements = addElements?.value !== '' ? [addElements?.value] : [];
    data.explicit_includes = explicitIncludes.map((e) => e.value);
    data.exclude_compositions = excludeCompositions.map((e) => e.value);
    // get values from pressure
    data.pressure = pressure;

    if (compoundMode === 'cif') {
      data.target_entry_id = null;
      if (cifString) {
        data.custom_entry_cif_string = cifString;
      } else {
        // prevent submission, cif string is required
        return;
      }
    } else {
      data.custom_entry_cif_string = null;
    }

    // set the form request to trigger an api call
    mutation.mutate(data);
  };
  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  // store the contents of the cif file into a string for later use
  const handleCIFLoad = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const file = event.target.files[0];
      const fileReader = new FileReader();
      setSelectedFile(file);
      fileReader.onload = function () {
        const content = fileReader.result;
        if (content && typeof content === 'string') {
          setCifString(content);
        }
      };

      if (file) {
        fileReader.readAsText(file);
      }
    }
  };

  return (
    /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
    <form onSubmit={handleSubmit(onSubmit)} className={styles.fullpage}>
      <div className={styles.Form}>
        <Tooltip />
        <div className={styles.FormGrid}>
          <div className={styles.firstrow}>
            <Toggle options={toggleOptions} onChange={setCompoundMode} value={compoundMode} />
            {compoundMode === 'compound' ? (
              <div className={styles.selectCSS}>
                <div>
                  <div className={styles.labelwithinfo}>
                    <label className={styles.label}>Target Compound (mp-id)*</label>
                    <InfoImage imagePath={logo} altText="Info" information={description.target_entry_id} />
                  </div>
                  <input
                    className={`${styles.inputfield} ${errors.target_entry_id ? styles.error : ''}`}
                    placeholder="mp-9029"
                    {...register('target_entry_id', { required: true })}
                  />
                  <p className={styles.error}>{errors.target_entry_id ? 'Formula field is required' : ''}</p>
                </div>
              </div>
            ) : (
              <>
                <div className={styles.FileUpload}>
                  <input
                    type="file"
                    accept=".cif"
                    name="cifFile"
                    required={true}
                    onChange={handleCIFLoad}
                    ref={fileInputRef}
                    className="hidden"
                  />
                  <button type="button" onClick={handleButtonClick} className={styles.choosefile}>
                    CHOOSE FILE
                  </button>
                  {selectedFile ? (
                    <span className="ml-2">{selectedFile.name}</span>
                  ) : (
                    <span className="ml-2">No .cif file chosen</span>
                  )}
                </div>
                <div className={styles.selectCSS}>
                  <div>
                    <div className={styles.labelwithinfo}>
                      <label className={styles.label}>Formation Energy Per Atom</label>
                    </div>
                    <input
                      type="number"
                      className={styles.inputfield}
                      {...register('custom_entry_formation_energy_per_atom', { valueAsNumber: true })}
                      defaultValue={0}
                    />
                  </div>
                </div>
              </>
            )}
            <div className={styles.selectCSS}>
              <div>
                <div className={styles.labelwithinfo}>
                  <label className={styles.label}>Temperature (K)*</label>
                </div>
                <input
                  type="number"
                  step="any"
                  className={`${styles.inputfield} ${errors.temperature ? styles.error : ''}`}
                  defaultValue={1000}
                  {...register('temperature', { valueAsNumber: true,required: true })}
                />
                <p className={styles.error}>{errors.temperature ? 'This field is required' : ''}</p>
              </div>
            </div>
            <div className={styles.selectCSS}>
              <div>
                <div className={styles.labelwithinfo}>
                  <label className={styles.label}>Maximum number of components in precursors*</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.max_component_precursors} />
                </div>
                <input
                  type="text"
                  className={`${styles.inputfield} ${errors.max_component_precursors ? styles.error : ''}`}
                  {...register('max_component_precursors', { valueAsNumber: true,required:true })}
                  defaultValue={0}
                />
                <p className={styles.error}>{errors.max_component_precursors ? 'This field is required' : ''}</p>
              </div>
            </div>
            <div className={styles.selectCSS}>
              <div>
                <div className={styles.labelwithinfo}>
                  <label className={styles.label}>Depth of parasitic reaction search*</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.flexible_competition} />
                </div>
                <input
                  className={`${styles.inputfield} ${errors.flexible_competition ? styles.error : ''}`}
                  {...register('flexible_competition', { valueAsNumber: true,required:true })}
                  defaultValue={0}
                />
                <p className={styles.error}>{errors.flexible_competition ? 'This field is required' : ''}</p>
              </div>
            </div>
            <div className={styles.selectCSS}>
              <div>
                <div className={styles.labelwithinfo}>
                  <label className={styles.label}>Distance to Hull (eV/atom)</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.hull_distance} />
                </div>
                <input
                  className={styles.inputfield}
                  {...register('hull_distance', { valueAsNumber: true })}
                  disabled={watchConfineToStables}
                  defaultValue={1000}
                />
              </div>
            </div>
            <div className={styles.selectCSS}>
              <div>
                <div className={styles.labelwithinfoforselect}>
                  <label className={styles.label}>Additional element to consider</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.add_elements} />
                </div>
                <SingleSelect value={addElements.value} options={addElementOptions} setValue={setAddElements} />
              </div>
            </div>
            <div className={styles.selectCSS}>
              <div>
                <div className={styles.labelwithinfoforselect}>
                  <label className={styles.label}>Explicitly include as precursor</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.explicit_includes} />
                </div>
                <MultiSelect placeholder="Type mp-id and press enter" setValues={setExplicitIncludes} />
              </div>
            </div>
          </div>
          <div className={styles.secondrow}>
            <div className={styles.Checkboxes}>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="allow_gas_release" control={control} defaultValue={false} />
                  <label className={styles.checklabel}> Allow for gaseous reaction products</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.allow_gas_release} />
                </div>
              </div>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="show_fraction_known_precursors" control={control} defaultValue={false} />
                  <label> Show the fraction of known precursors in reaction</label>
                </div>
              </div>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="show_known_precursors_only" control={control} defaultValue={false} />
                  <label> Show only reactions with known precursors</label>
                </div>
              </div>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="confine_to_stables" control={control} defaultValue={true} />
                  <label>Stable precursors only</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.confine_to_stables} />
                </div>
              </div>
              <div>
                <div className={styles.labelwithinfo}>
                  <FormCheckbox name="confine_to_icsd" control={control} defaultValue={true} />
                  <label> ICSD-based precursors only</label>
                  <InfoImage imagePath={logo} altText="Info" information={description.confine_to_icsd} />
                </div>
              </div>
            </div>
            <div className={styles.pressurerevamp}>
              <Pressure setPressure={setPressure} />
            </div>
          </div>
          <div>
            <AdvancedOptions
              control={control}
              compoundMode={compoundMode}
              register={register}
              setExcludeCompositions={setExcludeCompositions}
            />
          </div>
        </div>
      </div>
      <Button placeholder="Run" type="submit" className={styles.runbutton}>
        Run
      </Button>
    </form>
  );
}
