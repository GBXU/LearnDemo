package com.servlet.main;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.PreparedStatement;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.mysql.jdbc.Connection;
import com.servlet.bean.UserBean;
import com.servlet.util.Dbutil;

/**
 * Servlet implementation class Stop
 */
@WebServlet("/Stop")
public class Stop extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Stop() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String projectid = request.getParameter("projectid");
		HttpSession session = request.getSession(true);
		UserBean user = (UserBean)session.getAttribute("user");
		if(user==null || Integer.valueOf(projectid) != user.getUserId()){
			getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
		}
		
        try {  
            Connection con=(Connection) Dbutil.getConnection();  
            String sql="Update project Set status = '0' where projectid=?";
            PreparedStatement stmt=con.prepareStatement(sql);
            stmt.setInt(1, Integer.valueOf(projectid));
            int rs=stmt.executeUpdate();  
        }  
        catch(Exception ex) {  
            ex.printStackTrace();  
        }  
        finally {  
        	Dbutil.Close();  
        }
        String tmp = "/projectdetail.jsp?projectid="+projectid;
        getServletContext().getRequestDispatcher(tmp).forward(request, response);
	}

}
