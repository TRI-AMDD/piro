import { forwardRef, FC, ComponentPropsWithRef } from 'react';

export type InputProps = {
    /**
     * This shows a label above the input when provided.
     */
    label?: string;
    /**
     * If not empty, the input component will be displayed in an error state with the provided error message.
     */
    error?: string;
};

/**
 * Input Component
 *
 * The Input component takes in native input props as well as its own InputProps. The state is not managed
 * in this component and should be handled in the consuming app.
 *
 */
const Input: FC<InputProps & ComponentPropsWithRef<'input'>> = forwardRef(({ label, error = '', ...props }, ref) => (
    <div>
        {label && <span>{label}</span>}
        <input {...props} ref={ref} />
        <div>{error}</div>
    </div>
));

export default Input;
