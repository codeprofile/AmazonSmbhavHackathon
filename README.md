# ArtWork with NFT
<p> A portal and marketplace for local artists to sign in / register and upload their arts and descriptions and protect their arts by authenticating them with a crypto wallet based out of smart contract to secure their arts.</p>

<p><b>Below is the architecture diagram</b></p>

<img src="https://user-images.githubusercontent.com/94001814/167314032-29800227-cd30-4b89-b541-004a0448b834.png" width=45% height=40%>



Here In our application we ask : user/ artist to upload or generate their digital asset through `upload Asset` tab in the nav bar.


<img src="https://user-images.githubusercontent.com/94001814/167314639-4498bc7e-7686-4391-a06d-f3c662873a82.jpeg" width=75% height=75%>

After successfully uploaded digital asset call is forwarded to `NFT backend` module where meta data generation , smart contract generation and deploying on nodes takes places also the data are stored in dynamo DB and digital asset with meta data are stored in S3 bucket .

<p> In `NFT backend` module we create a local Ethereum network i.e ganache which creates accounts in the Hierarchical Deterministic (HD) wallet with ethers assigned to the account where we can check available Ethers in the account, send ethers to accounts in metamask wallet and smart contracts.</p>
<p> Truffle compiles the smart contract. We store the contract address as variable that the project retrieves to communicate with the smart contract. </p>



Now after uploading you either have option to navigate to `home` page or `Dashboard` page

<i><b>home : </b></i>Home page act as a market place for artwork from different artist where you can buy, sell , bid . 

<img src="https://user-images.githubusercontent.com/94001814/167314238-dd16150a-ef4b-4fe2-acb3-d02790766c2e.jpeg" width=75% height=75%>

<i><b>Dashboard : </b></i>Dashboard page gives you analysis of your historical transcation counts and records . 

<img src="https://user-images.githubusercontent.com/94001814/167314673-88469a15-2ced-4087-8f8a-f68d1f4a8741.jpeg" width=75% height=75%>


