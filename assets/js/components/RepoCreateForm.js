import React from 'react';
import PropTypes from 'prop-types';
import { Field, reduxForm } from 'redux-form';

const renderField = ({
  input: { name, value, onChange }, placeholder, className, type, meta: { touched, error, invalid },
}) => (
  <div>
    <input
      name={name}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className={`${className} ${touched && invalid ? 'is-invalid' : ''}`}
      type={type}
    />
    {touched
      && ((error && (
        <div className="invalid-feedback">
          {error}
        </div>
      )))}
  </div>
);

renderField.propTypes = {
  input: PropTypes.shape({
    name: PropTypes.string,
    value: PropTypes.string,
    onChange: PropTypes.func,
  }).isRequired,
  placeholder: PropTypes.string.isRequired,
  className: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  meta: PropTypes.shape({
    touched: PropTypes.bool,
    error: PropTypes.string,
    invalid: PropTypes.bool,
  }).isRequired,
};

const RepoCreateForm = (props) => {
  const {
    errorMessages, handleSubmit, pristine, submitting,
  } = props;

  const [errorToggled, setErrorToggled] = React.useState(false);
  const [successToggled, setSuccessToggled] = React.useState(false);
  const { username } = document.getElementById('main').dataset;

  const usernamePrefix = (value) => {
    const defaultValue = `${username}/`;
    if (!value) return value;
    return `${defaultValue}${value.split('/').slice(1).join()}`;
  };

  const toggleErrorDialog = () => {
    setErrorToggled(!errorToggled);
  };

  const toggleSucessDialog = () => {
    setSuccessToggled(!successToggled);
  };

  React.useEffect(() => {
    const dialog = !errorMessages ? setSuccessToggled : setErrorToggled;
    dialog(true);
  }, [errorMessages]);

  return (
    <div>
      <form onSubmit={handleSubmit} id="repoForm">
        <div className="form-row">
          <div className="col-10">
            <Field
              name="name"
              placeholder="Enter the repository name, must match {user}/{repo}"
              className="form-control"
              component={renderField}
              type="text"
              normalize={usernamePrefix}
            />
          </div>
          <div className="col-2">
            <button disabled={pristine || submitting} className="btn btn-block btn-dark" type="submit">
              Submit
            </button>
          </div>
        </div>
      </form>
      {errorMessages === false
        && (
          <div className={`alert-overlay ${successToggled && 'alert-overlay-toggle'}`}>
            <div className="popup text-success">
              <h4 className="text-success">Success!</h4>
              <button type="button" className="close text-success" onClick={toggleSucessDialog}>×</button>
              <div className="content">
                Repository added successfully!
              </div>
            </div>
          </div>
        )}
      {!!errorMessages && errorMessages.length
        && (
          <div className={`alert-overlay ${errorToggled && 'alert-overlay-toggle'}`}>
            <div className="popup text-danger">
              <h4 className="text-danger">Error!</h4>
              <button type="button" className="close text-danger" onClick={toggleErrorDialog}>×</button>
              <div className="content">
                { errorMessages.map((error) => (<span key={error}>{error}</span>)) }
              </div>
            </div>
          </div>
        )}
    </div>
  );
};

RepoCreateForm.defaultProps = {
  errorMessages: null,
};

RepoCreateForm.propTypes = {
  handleSubmit: PropTypes.func.isRequired,
  pristine: PropTypes.bool.isRequired,
  submitting: PropTypes.bool.isRequired,
  errorMessages: PropTypes.arrayOf(PropTypes.string),
};

const validate = (values) => {
  const { username } = document.getElementById('main').dataset;
  const errors = {};
  if (!values.name || !values.name.startsWith(`${username}/`)) {
    errors.name = `Repository must belong to you (eg: ${username}/repo-name)`;
  }
  return errors;
};

export default reduxForm({
  form: 'repoCreate',
  validate,
})(RepoCreateForm);
