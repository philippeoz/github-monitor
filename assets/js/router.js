import React from 'react';
import {
  BrowserRouter as Router, Route, Switch,
} from 'react-router-dom';
import CommitListContainer from './containers/CommitListContainer';
import RepoCreateContainer from './containers/RepoCreateContainer';
import SideBar from './components/SideBar';

const RouterComponent = () => {
  const [isToggled, setToggled] = React.useState(false);

  const toggleClass = () => {
    setToggled(!isToggled);
  };

  return (
    <Router>
      <div
        id="wrapper"
        className={isToggled ? 'toggled' : null}
      >

        <div id="sidebar-wrapper">
          <SideBar />
        </div>

        <div id="page-content-wrapper">
          <div className="container-fluid">
            <div className="row" style={{ flexWrap: 'nowrap' }}>
              <div className="col-1" style={{ maxWidth: 50 }}>
                <button type="button" className="btn btn-dark" onClick={toggleClass}>
                  ☰
                </button>
              </div>
              <div className="col-11 w-100" style={{ maxWidth: '100%', flexGrow: '1' }}>
                <RepoCreateContainer />
              </div>
            </div>
            <Switch>
              <Route path="/" exact component={CommitListContainer} />
            </Switch>
          </div>
        </div>

      </div>
    </Router>
  );
};

export default RouterComponent;
