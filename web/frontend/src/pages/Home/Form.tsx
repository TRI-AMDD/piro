import { useState } from 'react';
import { useForm, SubmitHandler } from 'react-hook-form';
import { Button } from '@material-tailwind/react';
import { Input, Toggle } from '@toyota-research-institute/lakefront';
import { Tooltip } from 'react-tooltip';

import styles from './Home.module.css';
import FormCheckbox from './Checkbox';
import { Inputs, PressureType, Option } from './TypeProps';

import MultiSelect from './MultiSelect';
import AdvancedOptions from './AdvancedOptions';
import Pressure from './Pressure';
import MoreInfo from './MoreInfo';
import { description } from './description';
import SingleSelect from './SingleSelect';
import { usePlotData } from './plotDataContext';
import { MultiValue } from 'react-select';

const addElementOptions = [
  { value: '', label: 'None' },
  { value: 'C', label: 'C' },
  { value: 'O', label: 'O' }
];

const toggleOptions = [
  { label: 'Target Compound', value: 'compound' },
  { label: '.cif File Upload', value: 'cif' }
];

export default function Form() {
  const { mutation } = usePlotData();
  const [pressure, setPressure] = useState<PressureType | null | number>(null);
  const [addElements, setAddElements] = useState<{ label: string; value: string }>();
  const [explicitIncludes, setExplicitIncludes] = useState<MultiValue<Option>>([]);
  const [excludeCompositions, setExcludeCompositions] = useState<MultiValue<Option>>([]);
  const [compoundMode, setCompoundMode] = useState('compound');
  const [cifString, setCifString] = useState<string>('');

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
    data.add_elements = addElements ? [addElements.value] : [];
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

  // store the contents of the cif file into a string for later use
  const handleCIFLoad = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const file = event.target.files[0];
      const fileReader = new FileReader();

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
        <div>
          <Toggle options={toggleOptions} onChange={setCompoundMode} value={compoundMode} />
          {compoundMode === 'compound' ? (
            <MoreInfo info={description.target_entry_id}>
              <Input
                label="Target Compound (mp-id)"
                placeholder="mp-9029"
                {...register('target_entry_id', { required: true })}
                error={errors.target_entry_id ? 'Formula field is required' : ''}
              />
            </MoreInfo>
          ) : (
            <>
              <div className={styles.FileUpload}>
                <Input
                  label="cif File"
                  type="file"
                  accept=".cif"
                  name="cifFile"
                  required={true}
                  onChange={handleCIFLoad}
                  className={styles.FileUpload}
                />
              </div>
              <Input
                type="number"
                step="any"
                label="Formation Energy Per Atom"
                {...register('custom_entry_formation_energy_per_atom', { valueAsNumber: true })}
              />
            </>
          )}

          <Input
            type="number"
            step="any"
            label="Temperature (K)"
            defaultValue={1000}
            {...register('temperature', { valueAsNumber: true })}
          />
          <MoreInfo info={description.max_component_precursors}>
            <Input
              label="Maximum number of components in precursors"
              {...register('max_component_precursors', { valueAsNumber: true })}
              defaultValue={0}
            />
          </MoreInfo>
          <MoreInfo info={description.flexible_competition}>
            <Input
              label="Depth of parasitic reaction search"
              {...register('flexible_competition', { valueAsNumber: true })}
              defaultValue={0}
            />
          </MoreInfo>
          <MoreInfo info={description.hull_distance}>
            <Input
              label="Distance to Hull (eV/atom)"
              {...register('hull_distance', { valueAsNumber: true })}
              disabled={watchConfineToStables}
              defaultValue={1000}
            />
          </MoreInfo>
          <MoreInfo info={description.add_elements}>
            <SingleSelect
              label="Additional element to consider"
              options={addElementOptions}
              setValue={setAddElements}
            />
          </MoreInfo>
          <MoreInfo info={description.explicit_includes}>
            <MultiSelect
              label="Explicitly include as precursor"
              placeholder="Type mp-id and press enter"
              setValues={setExplicitIncludes}
            />
          </MoreInfo>
        </div>
        <div className={styles.secondrow}>
          <div className={styles.Checkboxes}>
          <MoreInfo info={description.allow_gas_release} isCheckbox>
            <FormCheckbox
              name="allow_gas_release"
              control={control}
              label="Allow for gaseous reaction products"
              defaultValue={false}
            />
          </MoreInfo>
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
          <MoreInfo info={description.confine_to_stables} isCheckbox>
            <FormCheckbox
              name="confine_to_stables"
              control={control}
              label="Stable Precursors Only"
              defaultValue={true}
            />
          </MoreInfo>
          <MoreInfo info={description.confine_to_icsd} isCheckbox>
            <FormCheckbox
              name="confine_to_icsd"
              control={control}
              label="ICSD-based Precursors Only"
              defaultValue={true}
            />
          </MoreInfo>
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
      

      <Button placeholder="Run" type="submit">
        Run
      </Button>
    </form>
  );
}
