import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import RouterComponent from './router';
import store from './store';

ReactDOM.render(
  <Provider store={store}>
    <RouterComponent />
  </Provider>,
  document.getElementById('main'),
);
