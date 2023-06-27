import { Outlet, useNavigate } from "react-router-dom";

export default function Root() {
  const navigate = useNavigate()


    return (
        <>
          <nav className="navbar navbar-expand-lg bg-body-tertiary">
            <div className="container-fluid">
              <a className="navbar-brand" href="#">Inventory</a>
              <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
              </button>
              <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                  <li className="nav-item">
                    <a className="nav-link active" aria-current="page" href="#">All Items</a>
                  </li>
                  <li className="nav-item">
                    <a className="nav-link disabled">Your Items</a>
                  </li>
                </ul>
                <button type="button" class="btn btn-outline-primary" onClick={() => {navigate("/login")}}>Log In</button>
                <button type="button" class="btn btn-outline-primary" onClick={() => {navigate("/createAccount")}}>Create Account</button>
              </div>
            </div>
          </nav>
          <div className="container">
          <Outlet />
            </div>
</>
    );
  }